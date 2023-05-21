#!/usr/bin/env python3
import subprocess
import json
import requests
import os
BearerToken = os.getenv('BearerToken')

dict_Port = {}
json_string = ""


# Define the API endpoint URL
url = "http://192.168.8.174:5000/api/portscan"
ArrPorts=["80", "443", "21", "23", "25", "110", "143", "53", "194", "119", "389", "161", "22"]

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

            pass

def create_json_string():
    print("Create Json string")
    # Create json string format
    data = {
         "IpAdress": ip_address,
         "MacAdress": mac_address,
         "Ports": dict_Port
        }
    print(data)
        # crate json string
    global json_string
    json_string = json.dumps(data, indent=2)
    print(json_string)

print("start")
# Check if nmap is installed
if not subprocess.run(["which", "nmap"], capture_output=True, text=True).stdout.strip():
    print("nmap is not installed, installing")
    subprocess.run(["sudo", "apt-get", "update"])
    subprocess.run(["sudo", "apt-get", "install", "-y", "nmap"])

# Get the IP address of the device
ip_address = "192.168.1.1"
print(ip_address)

# Get the MAC address of the device
mac_address = "28-EE-52-25-DB-56"
print(mac_address)
for ports in ArrPorts:
    result = subprocess.run(["sudo", "nmap","st", "-p", ports, ip_address], capture_output=True, text=True)
    print(result)
 #Extract the open and closed ports and update dict_Ports)
    output_lines = result.stdout.split("\n")
    status_line = [line for line in output_lines if "tcp" in line and ports in line][0]
    status = status_line.split()[1]
    dict_Port.update({ports: status})

create_json_string()
Send_json()
