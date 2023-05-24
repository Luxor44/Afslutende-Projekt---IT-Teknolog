#!/usr/bin/env python3
import os
import requests
BearerToken = os.getenv('BearerToken')
url = "http://192.168.8.174:5000/api/get/portscan"


def get_api_data():
    headers = {"Authorization": "Bearer "+BearerToken, "Content-Type": "application/json"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print('Error: Unable to retrieve data from API')
        return None

# assign each item in the data recieved
data = get_api_data()
if data:
    for item in data:
        ip_address = item['IpAdress']
        mac_address = item['MacAdress']
        ports = item['Ports']
        id = item['id']
        Datetime = item['Datetime']
        print(f'Item {id}: IP Address={ip_address}, MAC Address={mac_address}, Ports={ports}')
