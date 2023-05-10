#!/usr/bin/env python3

import vonage
import string
import random
import os
from functools import wraps
import json
import requests

BearerToken = os.getenv('BearerToken')
vonageKey = os.getenv('vonageKey')
vonageSecret = os.getenv('vonageSecret')

#Get username and password from request
Username = "Luxor"
Password = "123"
url = "http://192.168.8.163:5000/api/Login"

#login
headers = {"Authorization": "Bearer "+BearerToken, "Content-Type": "application/json"}
#headers = {"Content-Type": "application/json", "Authorization": BearerToken}
payload = {"Username": Username, "Password": Password}

response = requests.post(url, headers=headers, data=json.dumps(payload))
print(response.text)
if response.status_code == 200:
    print("Request succeeded")
    user = response.json()
    #Phone_number = user["Number"]
    print(user)
    user_list = json.loads(user)
    Phone_number = user_list[0]
    print(user)
#else:
#    print("Request failed with status code : ", response.status.code)

    if user == None:
        print("Wrong username or password")
    else:
        #random MFA string
        random_string = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        #Vonage API : https://dashboard.nexmo.com/
        #change the key string and secret string to the os.getenv vonageKey and vonageSecret
        client = vonage.Client(key= vonageKey, secret= vonageSecret)
        sms = vonage.Sms(client)

        responseData = sms.send_message(
        {
                "from": "Vonage APIs",
                "to": "45" + Phone_number,
                "text": "Your MFA code is: " + random_string,
        }
        )

        if responseData["messages"][0]["status"] == "0":
            print("Message sent successfully.")
        else:
            print(f"Message failed with error: {responseData['messages'][0]['error-text']}")
            #Validate MFA CODE
            #mfa_code = input('Enter the MFA code that was sent by SMS: ')
            #if mfa_code = random_string:
            #    print("MFA code validated")
            #else:
            #    print("inconnect MFA code")

else:
    print("Request failed with status code : " + response.status.code)
