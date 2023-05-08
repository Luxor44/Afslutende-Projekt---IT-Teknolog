#!/usr/bin/env python3

import vonage
import string
import random
import os

from functools import wraps
import json
import requests


BearerToken = "Bearer:eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
#vonageKey = os.getenv('vonageKey')
#vonageSecret = os.getenv('vonageSecret')

#Get username and password from request
Username = "Luxor"
Password = "123"
url = "http://192.168.8.163:5000/api/Login"

#login
headers = {"Authorization": "Bearer"+BearerToken, "Content-Type": "application/json"}
#headers = {"Content-Type": "application/json", "Authorization": BearerToken}
payload = {"Username": Username, "Password": Password}

response = requests.post(url, headers=headers, data=json.dumps(payload))
print(response.text)
if response.status_code == 200:
    print("Request succeeded")
    user = response.json()
    Phone_number = user["Number"]
else:
    print("Request failed with status code : ", response.status.code)

    if user == None:
        print("Wrong username or password")
    else:
        #random MFA string
        random_string = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        #Vonage API : https://dashboard.nexmo.com/
        #change the key string and secret string to the os.getenv vonageKey and vonageSecret
        client = vonage.Client(key="8be7c1af", secret="5KqNcnphiaLxLPPs")
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
