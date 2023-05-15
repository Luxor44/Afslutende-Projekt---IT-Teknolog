#!/usr/bin/env python3

import json
import requests
import os
import hashlib
h = hashlib.sha256()
BearerToken = os.getenv('BearerToken')

Username = "luxor"
Password = "123"
Password = Password.encode('utf-8')
Password = h.update(Password)
Password = h.hexdigest()
Phonenumber = "27571028"

url = "http://192.168.8.174:5000/api/add/user"

def Send_json():
    print("send_json start")
# Set the Content-Type request header to specify JSON data
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + BearerToken
    }

              # Make the POST request
    response = requests.post(url, data=json_string, headers=headers)

    # Check the response status code
    if response.status_code == 200:
               # success_count += 1
        try:
            print("sending : " + json_string)
        # can i remove this line? since we are not sending files anymore
        except FileNotFoundError:

def create_json_string():
    print("Create Json string")
    # Create json string format
    data = {
         "username": Username,
         "password": Password,
         "phonenumber": Phonenumber
        }
    print(data)
        # crate json string
    global json_string
    json_string = json.dumps(data, indent=2)
    print(json_string)
    
create_json_string()
Send_json()
           
