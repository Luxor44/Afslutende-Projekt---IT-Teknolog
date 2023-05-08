import json
import requests
import os 

BearerToken = os.getenv('BearerToken')

# Define the API endpoint URL
url = "http://192.168.8.163:5000/api/portscan"

# Set the Content-Type request header to specify JSON data
headers = {
    "Content-Type": "application/json"
    "Authorization": BearerToken
}

# Loop through all the JSON files and make separate POST requests
for port_number in range(1, 10000):
    filename = str(port_number) + ".json"
    try:
        # Open the JSON file and read the data
        with open(filename, "r") as f:
            payload = json.load(f)
        
        # Make the POST request
        response = requests.post(url, data=json.dumps(payload), headers=headers)

        # Check the response status code
        if response.status_code == 200:
            print("Request succeeded for payload in file:", filename)
        else:
            print("Request failed with status code", response.status_code, "for payload in file:", filename)
    except FileNotFoundError:
        # Skip if the JSON file does not exist
        pass
