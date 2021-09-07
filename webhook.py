from flask import Flask,request
import json
import requests
from rasa import *
from pymessenger import Bot
import pandas as pd
import random
import sqlite3
import time
import logging



LOG_FILENAME = 'covidbot.log'
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)

print("Covid bot running")

bot_version = ''

bots= {'india':""}

token = 'EAAHpNe7gFQ4BAFkzyeZCVxKGEXSZBdlTGtQ8mlxuCMVQK7S20loAeiBhhnUhSx7ZAA6pcXgkGtOVzuLOlXsUlWgKlqbRTpbGfG7GtZBLZBANlHdR6sMAXkQpVhZCDSaJZAvEWaguSeSbEJPbRu5yugntNIIoyBnLYm5BxOl62IGhgZDZD'

app = Flask(__name__)

VERIFY_TOKEN = 'covid'

#pageid of srutipic->search in about
def send_messenger_final_response(response, id):
    headers = {"Content-type": "application/json"}
    data_json = {"recipient": {"id":id},"message":{"text":response}}
    r = requests.post(url = "https://graph.facebook.com/101948504825522/messages?access_token="+token,data = json.dumps(data_json), headers = headers)
    print(r.text)  

def new_user_check(sender_id):
    conn = sqlite3.connect('F:\sqlite\COVID19_DB.db')
    cursor = conn.cursor()
    conversation_id = None
    user_name = None
    df = pd.read_sql("select User_ID, User_Name, Conversation_ID from COVID19_USER_DETAILS where user_id =" + sender_id, conn)
    if(df.shape[0] == 0):
        print("************************************************NEW USER******************************************")
        conversations = requests.get("https://graph.facebook.com/101948504825522?fields=conversations.limit(100){senders,link,id}&access_token="+token)
        Conversation_Link = None
        conversation_id = None
        email = None
        mobile_number = None
        pincode = None

        for i in conversations.json()["conversations"]["data"]:
            flag = False
            conversation_id = i["id"]
            for j in i["senders"]["data"]:
                if(j["id"] == '101948504825522'):
                    pass
                elif j["id"] == sender_id:
                    user_name = j["name"]
                    Conversation_Link = "http://facebook.com" + i["link"]
                    flag = True
                    break
                
            if(flag):
                break
            
        df2 = pd.read_sql("select count(*) from COVID19_USER_DETAILS", conn)
        row_id = df2.iloc[0][0] + 1
        cursor.execute("insert into COVID19_USER_DETAILS (ROW_ID,USER_ID,USER_NAME,CONVERSATION_ID,CONVERSATION_LINK) values (" + str(row_id) + ", " + sender_id +", '" + user_name + "', '" + conversation_id + "', '" + Conversation_Link + "')")
        conn.commit()
		
    else:
        user_name = df.iloc[0][1]
        conversation_id = df.iloc[0][2]
    conn.close()
    return user_name,conversation_id

def insert_into_messenger(timestamp,hr_timestamp,conversation_id,sender_id,user_name,message_text,final_response):
    if final_response is None:
        final_response = "None"
    conn = sqlite3.connect('F:\sqlite\COVID19_DB.db')
    cursor = conn.cursor()
    df = pd.read_sql("select count(*) from COVID19_MESSANGER", conn)
    row_id = df.iloc[0][0] + 1
    cursor.execute("insert into COVID19_MESSANGER (row_id,timestamp,hr_timestamp,conversation_id,user_id,user_name,input,response) values (" + str(row_id) + ", " + str(timestamp) + ", '" + hr_timestamp + "', '" + conversation_id + "', " + sender_id + ", '" + user_name + "', '" + message_text + "', '" + final_response + "')")
    conn.commit()
    conn.close()
	
def verify_fb_token(token_sent):
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'

@app.route("/", methods = ['GET','POST'])
def getResponse():
    enablepermission = True
    if request.method.lower == 'get':
        verify_token = request.args.get("hub.verify_token")
        return verify_fb_token(verify_token)
    else:
        try:
            data = request.get_json()
            print(json.dumps(data,indent=2))
            if data["object"] == "page":
                if "messaging" in data["entry"][0]:
                    print("Checked data[object] == page")
                    for entry in data["entry"]:
                        print("inside first for loop")
                        for messaging_event in entry["messaging"]:
                            print("inside second loop")
                            if messaging_event.get("message"): #This tells us the message event is obtained in the page messenger
                                print("inside last if")
                                sender_id = messaging_event["sender"]["id"]
                                #recipient_id = messaging_event["recipient"]["id"]
                                timestamp = messaging_event["timestamp"]
                                timestamp = int(str(timestamp)[:10])
                                message_text = messaging_event["message"]["text"]
                                hr_timestamp = time.strftime("%d %b %Y %H:%M:%S", time.localtime(timestamp))
                                print("**********************The messenger message****************" + message_text)
                                user_name,conversation_id = new_user_check(sender_id)
								
                                final_response = pre_process(message_text.lower(),timestamp,hr_timestamp,sender_id,user_name)
                                print("***********************Bot Response**************************: ", end= '')
                                print(final_response)
                                if final_response is not None:
                                    send_messenger_final_response(final_response, sender_id)
                                insert_into_messenger(timestamp,hr_timestamp,conversation_id,sender_id,user_name,message_text,final_response)
        except Exception as e:
            print("some error occured")
            print(e)
            
    return "200 OK HTTPS"


@app.route("/train")
def train_rasa():
    try:
        from rasa_nlu.training_data import load_data
        from rasa_nlu import config
        from rasa_nlu.config import RasaNLUModelConfig
        from rasa_nlu.model import Trainer
        from rasa_nlu.model import Metadata, Interpreter
        logging.debug("The training component invoked")
        training_data = load_data('./nld.md')
        trainer = Trainer(config.load('config.yml'))
        trainer.train(training_data)
        model_directory = trainer.persist('./models/nlu/', fixed_model_name = 'current')
        interpreter = Interpreter.load('./models/nlu/default/current')
        print(interpreter.parse(u"hi"))
        logging.debug("The Chatbot Training is successful")
        
        print("Chatbot Training Successful")
        return "Chatbot Training Successful"
    
    except Exception as e:
        logging.error("The error occured in training the bot")
        print("Error occured in training chatbot")
        print(e)
    
if __name__ == '__main__':
    app.run(debug=True, port=80)