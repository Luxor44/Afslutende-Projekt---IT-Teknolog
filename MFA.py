import vonage
import string
import random
import os
from flask import Flask, jsonify, request
import mysql.connector
from functools import wraps

app = Flask(__name__)

SqlPassword = os.getenv('SqlPassword')
SqlUsername = os.getenv('SqlUsername')
BearerToken = os.getenv('BearerToken')
vonageKey = os.getenv('vonageKey')
vonageSecret = os.getenv('vonageSecret')

        #Get username and password from request
Username = request.form['username']
Password = request.form['password']
url = 'http://URL.com/api/Login"

#login
headers = {
        "Content=Type": "application/json"
        "Authorization": BearerToken
}
response = request.get(url, params={"Username": Username, "Password": Password}, headers=headers)
if respense.status_code == 201:
        print("Request succeeded")
        user = response.json()
        Phone_number = user["Number"]
else:
        print("Request failed with status code : ", response.status.code,
  
if user is None:
        Print("Wrong username or password")
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
        mfa_code = input('Enter the MFA code that was sent by SMS: ')
        if mfa_code = random_string:
                print("MFA code validated")
        else:
                print("inconnect MFA code")
