# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 12:49:53 2019

@author: Kanha
"""

import sqlite3
import pandas as pd
from rasa_nlu.model import Interpreter
import json
from pyshorteners import Shortener
import requests
from bs4 import BeautifulSoup 

def intent_identifier(input_message):
    interpreter = Interpreter.load("models/nlu/default/current/")
    result = interpreter.parse(input_message.lower())
    return result


def extract_statewise(input_state):
    state_name = input_state.capitalize() 
    url = 'https://www.mohfw.gov.in/'
    web_content = requests.get(url).content
    soup = BeautifulSoup(web_content, "html.parser")
    extract_contents = lambda row: [x.text.replace('\n', '') for x in row]
    stats = [] # initialize stats
    all_rows = soup.find_all('tr') # find all table rows 
    for row in all_rows: 
        stat = extract_contents(row.find_all('td')) # find all data cells  
    # notice that the data that we require is now a list of length 5
        if len(stat) == 5: 
            stats.append(stat)
    new_cols = ["Sr.No", "States/UT","Confirmed","Recovered","Deceased"]
    state_data = pd.DataFrame(data = stats, columns = new_cols)
	# converting the 'string' data to 'int'
    state_data['Confirmed'] = state_data['Confirmed'].map(int)
    state_data['Recovered'] = state_data['Recovered'].map(int)
    state_data['Deceased']  = state_data['Deceased'].map(int)
    intermediate = state_data.loc[state_data["States/UT"] == state_name]
    intermediate.reset_index(drop=True, inplace=True)
    #Confirmed = intermediate["Confirmed"]
    #Recovered = intermediate["Recovered"]
    #Deceased = intermediate["Deceased"]
    response = """Covid-19 Cases in {} \n\nConfirmed Cases : {} \n\nDeaths : {} \n\nRecovered : {} \n\n 👉 Type *S* to check cases in Other States. \n 👉 Type *A, B, C, E, F, G* to see other options \n 👉 Type *Menu* to view the Main Menu""".format(state_name,intermediate["Confirmed"].values[0],intermediate["Deceased"].values[0],intermediate["Recovered"].values[0])
    return response


		
def pre_process(sentence,timestamp,hr_timestamp,user_id,user_name):
    conn = sqlite3.connect('F:\sqlite\COVID19_DB.db',timeout=1)
    cursor = conn.cursor()
    final_Bot_Response = None
    responded = False
    state = ''
    intent_result = intent_identifier(sentence)
    print("+++++++++++++++++++++++++++ RASA Results +++++++++++++++++++++")
    print(json.dumps(intent_result, indent = 2))
    print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
	
    
    #Scenario 1: Greet
    if((intent_result)["intent"]["name"] == "greet" and intent_result["intent"]["confidence"] > 0.50):	 
        with open("responses.json",encoding="utf8") as f:
            dictionary = json.load(f)
        final_Bot_Response = dictionary["greet"]
        print(final_Bot_Response)
		
    #Scenario 2: What Is 
    if((intent_result)["intent"]["name"] == "what_is" and intent_result["intent"]["confidence"] > 0.50):         
        with open("responses.json",encoding="utf8") as f:
            dictionary = json.load(f)
        final_Bot_Response = dictionary["what_is"]
    
    #Scenario 3: how_spread
    if((intent_result)["intent"]["name"] == "how_spread" and intent_result["intent"]["confidence"] > 0.50):
        with open("responses.json",encoding="utf8") as f:
            dictionary = json.load(f)
        final_Bot_Response = dictionary["how_spread"]
    
    #Scenario 4: spread_no_sick
    if((intent_result)["intent"]["name"] == "spread_no_sick" and intent_result["intent"]["confidence"] > 0.50):
        with open("responses.json",encoding="utf8") as f:
            dictionary = json.load(f)
        final_Bot_Response = dictionary["spread_no_sick"]
    
    #Scenario 5: spread_objects
    if((intent_result)["intent"]["name"] == "spread_objects" and intent_result["intent"]["confidence"] > 0.50):
        with open("responses.json",encoding="utf8") as f:
            dictionary = json.load(f)
        final_Bot_Response = dictionary["spread_objects"]
    	
    #Scenario 6: spread_after_quarantine
    if((intent_result)["intent"]["name"] == "spread_objects" and intent_result["intent"]["confidence"] > 0.50):
        with open("responses.json",encoding="utf8") as f:
            dictionary = json.load(f)
        final_Bot_Response = dictionary["spread_objects"]
    	
    #Scenario 7: symptoms
    if((intent_result)["intent"]["name"] == "symptoms" and intent_result["intent"]["confidence"] > 0.50):
        with open("responses.json",encoding="utf8") as f:
            dictionary = json.load(f)
        final_Bot_Response = dictionary["symptoms"]
    
    #Scenario 8: what_to_do
    if((intent_result)["intent"]["name"] == "what_to_do" and intent_result["intent"]["confidence"] > 0.50):
        with open("responses.json",encoding="utf8") as f:
            dictionary = json.load(f)
        final_Bot_Response = dictionary["what_to_do"]
    
    #Scenario 9: most_at_risk
    if((intent_result)["intent"]["name"] == "most_at_risk" and intent_result["intent"]["confidence"] > 0.50):
        with open("responses.json",encoding="utf8") as f:
            dictionary = json.load(f)
        final_Bot_Response = dictionary["most_at_risk"]
    	
    #Scenario 10: poultry
    if((intent_result)["intent"]["name"] == "poultry" and intent_result["intent"]["confidence"] > 0.50):
        with open("responses.json",encoding="utf8") as f:
            dictionary = json.load(f)
        final_Bot_Response = dictionary["poultry"]
    	
    #Scenario 11: children
    if((intent_result)["intent"]["name"] == "children" and intent_result["intent"]["confidence"] > 0.50):
        with open("responses.json",encoding="utf8") as f:
            dictionary = json.load(f)
        final_Bot_Response = dictionary["children"]
    	
    #Scenario 12: medications
    if((intent_result)["intent"]["name"] == "medications" and intent_result["intent"]["confidence"] > 0.50):
        with open("responses.json",encoding="utf8") as f:
            dictionary = json.load(f)
        final_Bot_Response = dictionary["medications"]
    	
    #Scenario 13: masks
    if((intent_result)["intent"]["name"] == "masks" and intent_result["intent"]["confidence"] > 0.50):
        with open("responses.json",encoding="utf8") as f:
            dictionary = json.load(f)
        final_Bot_Response = dictionary["masks"]
    	
    #Scenario 14: incubation
    if((intent_result)["intent"]["name"] == "incubation" and intent_result["intent"]["confidence"] > 0.50):
        with open("responses.json",encoding="utf8") as f:
            dictionary = json.load(f)
        final_Bot_Response = dictionary["incubation"]
    	
    #Scenario 15: prevention
    if((intent_result)["intent"]["name"] == "prevention" and intent_result["intent"]["confidence"] > 0.50):
        with open("responses.json",encoding="utf8") as f:
            dictionary = json.load(f)
        final_Bot_Response = dictionary["prevention"]
    	
    #Scenario 16: dryers
    if((intent_result)["intent"]["name"] == "dryers" and intent_result["intent"]["confidence"] > 0.50):
        with open("responses.json",encoding="utf8") as f:
            dictionary = json.load(f)
        final_Bot_Response = dictionary["dryers"]
    	
    #Scenario 17: water
    if((intent_result)["intent"]["name"] == "water" and intent_result["intent"]["confidence"] > 0.50):
        with open("responses.json",encoding="utf8") as f:
            dictionary = json.load(f)
        final_Bot_Response = dictionary["water"]
    
    #Scenario 18: pets
    if((intent_result)["intent"]["name"] == "pets" and intent_result["intent"]["confidence"] > 0.50):
        with open("responses.json",encoding="utf8") as f:
            dictionary = json.load(f)
        final_Bot_Response = dictionary["pets"]
    	
    #Scenario 19: Thank
    if((intent_result)["intent"]["name"] == "thank" and intent_result["intent"]["confidence"] > 0.50):
        with open("responses.json",encoding="utf8") as f:
            dictionary = json.load(f)
        final_Bot_Response = dictionary["thanks"]
        
    #Scenario 20: Bye
    if((intent_result)["intent"]["name"] == "bye" and intent_result["intent"]["confidence"] > 0.50):
        with open("responses.json",encoding="utf8") as f:
            dictionary = json.load(f)
        final_Bot_Response = dictionary["bye"]
        
    #Scenario 21: Not Sure
    if((intent_result)["intent"]["name"] == "notsure" and intent_result["intent"]["confidence"] > 0.50):
        with open("responses.json",encoding="utf8") as f:
            dictionary = json.load(f)
        final_Bot_Response = dictionary["notsure"]
    
	#Scenario 22 : State
    if((intent_result)["intent"]["name"] == "state" and intent_result["intent"]["confidence"] > 0.50):
        if len(intent_result["entities"]) != 0:
            for i in intent_result["entities"]:
                if(i["entity"] == "state"):
                    state = (i["value"])
        final_Bot_Response = extract_statewise(state)
		
		
    if(intent_result["intent"]["confidence"] == 0.0):
        incoming_msg = intent_result["text"].upper()
        if 'A' in incoming_msg:
        # return total cases
            r = requests.get('https://coronavirus-19-api.herokuapp.com/all')
            if r.status_code == 200:
                data = r.json()
                text = f'_Covid-19 Cases Worldwide_ \n\nConfirmed Cases : *{data["cases"]}* \n\nDeaths : *{data["deaths"]}* \n\nRecovered : *{data["recovered"]}*  \n\n 👉 Type *B* to check cases in *India* \n 👉 Type *B, C, D, E, F, G* to see other options \n 👉 Type *Menu* to view the Main Menu'
                print(text)
            else:
                text = 'I could not retrieve the results at this time, sorry.'
            final_Bot_Response = text
            print(final_Bot_Response)
            responded = True
		
        if 'B' in incoming_msg or 'India' in incoming_msg:
            # return cases in india
            r = requests.get('https://coronavirus-19-api.herokuapp.com/countries/india')
            if r.status_code == 200:
                data = r.json()
                text = f'_Covid-19 Cases in India_ \n\nConfirmed Cases : *{data["cases"]}* \n\nToday Cases : *{data["todayCases"]}* \n\nDeaths : *{data["deaths"]}* \n\nRecovered : *{data["recovered"]}* \n\n 👉 Type *C* to check cases in *China* \n 👉 Type *A, C, D, E, F, G* to see other options \n 👉 Type *Menu* to view the Main Menu'
            else:
                text = 'I could not retrieve the results at this time, sorry.'
            final_Bot_Response = text
            print(final_Bot_Response)
            responded = True	
	    
        if 'C' in incoming_msg or 'China' in incoming_msg:
            # return cases in china
            r = requests.get('https://coronavirus-19-api.herokuapp.com/countries/china')
            if r.status_code == 200:
                data = r.json()
                text = f'_Covid-19 Cases in China_ \n\nConfirmed Cases : *{data["cases"]}* \n\nToday Cases : *{data["todayCases"]}* \n\nDeaths : *{data["deaths"]}* \n\nRecovered : *{data["recovered"]}* \n\nActive Cases : *{data["active"]}* \n\n 👉 Type *D* to check cases in *USA* \n 👉 Type *A, B, D, E, F, G* to see other options \n 👉 Type *Menu* to view the Main Menu'
            else:
                text = 'I could not retrieve the results at this time, sorry.'
            final_Bot_Response = text
            print(final_Bot_Response)
            responded = True
			
        if 'D' in incoming_msg or 'USA' in incoming_msg:
            # return cases in usa
            r = requests.get('https://coronavirus-19-api.herokuapp.com/countries/usa')
            if r.status_code == 200:
                data = r.json()
                text = f'_Covid-19 Cases in USA_ \n\nConfirmed Cases : *{data["cases"]}* \n\nToday Cases : *{data["todayCases"]}* \n\nDeaths : *{data["deaths"]}* \n\nRecovered : *{data["recovered"]}* \n\nActive Cases : *{data["active"]}*  \n\n 👉 Type *E* to check cases in *Italy* \n 👉 Type *A, B, C, E, F, G* to see other options \n 👉 Type *Menu* to view the Main Menu'
            else:
                text = 'I could not retrieve the results at this time, sorry.'
            final_Bot_Response = text
            print(final_Bot_Response)
            responded = True
            
        if 'E' in incoming_msg or 'Italy' in incoming_msg:
            # return cases in italy
            r = requests.get('https://coronavirus-19-api.herokuapp.com/countries/italy')
            if r.status_code == 200:
                data = r.json()
                text = f'_Covid-19 Cases in Italy_ \n\nConfirmed Cases : *{data["cases"]}* \n\nToday Cases : *{data["todayCases"]}* \n\nDeaths : *{data["deaths"]}* \n\nRecovered : *{data["recovered"]}* \n\nActive Cases : *{data["active"]}* \n\n 👉 Type *F* to check how *Covid-19 Spreads?* \n 👉 Type *A, B, C, E, F, G* to see other options \n 👉 Type *Menu* to view the Main Menu'
            else:
                text = 'I could not retrieve the results at this time, sorry.'	
            final_Bot_Response = text
            print(final_Bot_Response)
            responded = True
			
        if 'F' in incoming_msg or 'How does it Spread?' in incoming_msg:
            text = f'_Coronavirus spreads from an infected person through_ 👇 \n\n ♦ Small droplets from the nose or mouth which are spread when a person coughs or sneezes \n\n ♦ Touching an object or surface with these droplets on it and then touching your mouth, nose, or eyes before washing your hands \n \n ♦ Close personal contact, such as touching or shaking hands \n Please watch the video for more information 👇 https://youtu.be/0MgNgcwcKzE \n\n 👉 Type G to check the *Preventive Measures* \n 👉 Type *A, B, C, D, E* to see other options \n 👉 Type *Menu* to view the Main Menu'
            final_Bot_Response = text
            print(final_Bot_Response)
            responded = True
			
        if 'G' in incoming_msg:
            text = f'_Coronavirus infection can be prevented through the following means_ 👇 \n ✔️ Clean hand with soap and water or alcohol-based hand rub \n https://youtu.be/EJbjyo2xa2o \n\n ✔️ Cover nose and mouth when coughing & sneezing with a tissue or flexed elbow \n https://youtu.be/f2b_hgncFi4 \n\n ✔️ Avoid close contact & maintain 1-meter distance with anyone who is coughing or sneezin \n https://youtu.be/mYyNQZ6IdRk \n\n ✔️ Isolation of persons traveling from affected countries or places for at least 14 day \n https://www.mohfw.gov.in/AdditionalTravelAdvisory1homeisolation.pdf \n\n ✔️ Quarantine if advise \n https://www.mohfw.gov.in/Guidelinesforhomequarantine.pdf \n\n 👉 Type *A, B, C, D, E, F* to see other option \n 👉 Type *Menu* to view the Main Menu'
            final_Bot_Response = text
            print(final_Bot_Response)
            responded = True
			
        if 'MENU' in incoming_msg:
            with open("responses.json",encoding="utf8") as f:
                dictionary = json.load(f)
            final_Bot_Response = dictionary["greet"]
            print(final_Bot_Response)
            responded = True
			
        '''if 'PREVENTIVE MEASURES' in incoming_msg:
            with open("responses.json",encoding="utf8") as f:
                dictionary = json.load(f)
            final_Bot_Response = dictionary["prevention"]
            print(final_Bot_Response)
            responded = True'''
			
        if 'statewise info ' in incoming_msg or 'S' in incoming_msg:
	        return "Enter your state name"
			
        if responded == False:
            with open("responses.json",encoding="utf8") as f:
                dictionary = json.load(f)
            final_Bot_Response = dictionary["notsure"]
        return final_Bot_Response
					
    return final_Bot_Response

        

            