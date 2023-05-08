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


def require_token(func):
        @wraps(func)
        def decorated(*args, **kwargs):
                Token = None
                if 'Authorization' in request.headers:
                        auth_header = request.headers['Authorization']
                        Token = auth_header.split(" ")[1]
                if not Token:
                        return jsonify({'message': 'Token is missing'}), 401
                if Token != BearerToken:
                        return jsonify({'message': 'Token is invalid'}), 401
                return func(*args, **kwargs)
        return decorated

#login

@app.route('/api/login', methods=['GET'])
@require_token
def login():

        #Get username and password from request
        username = request.form['username']
        password = request.form['password']

            # connect to database
        conn = mysql.connector.connect(
        host='localhost',
        user=SqlUsername,
        password=SqlPassword,
        database='Login'
        )
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = c.fetchone()
if user is None:
        Print("Wrong username or password")
else:
        #random MFA string
        random_string = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        #Vonage API : https://dashboard.nexmo.com/
        client = vonage.Client(key="8be7c1af", secret="5KqNcnphiaLxLPPs")
        sms = vonage.Sms(client)

        responseData = sms.send_message(
        {
                "from": "Vonage APIs",
                "to": "4527571028",
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
