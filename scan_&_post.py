import subprocess
import json
import requests
import os
import array
BearerToken = os.getenv('BearerToken')






# Define the API endpoint URL
url = "http://192.168.8.163:5000/api/portscan"
ArrPorts=["80", "443", "21", "23", "25", "110", "143", "53", "194", "119", "389", "161", "22"]

def Send_json():
    print("send_json start")
# Set the Content-Type request header to specify JSON data
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + BearerToken
    }

    # Loop through all the JSON files and make separate POST requests
    for port_number in ArrPorts:
        filename = str(port_number) + ".json"
        print("trying to send : " + filename)
        try:
            print("inside the try : " + filename)
            # Open the JSON file and read the data
            with open(filename, "r") as f:
                payload = json.load(f)
                print("open the file to send and write : " + filename)

            # Make the POST request
            response = requests.post(url, data=json.dumps(payload), headers=headers)

            # Check the response status code
            if response.status_code == 200:
               # success_count += 1
                print("sending : " + filename)
            #else:
            #    fail_count += 1
        except FileNotFoundError:
            # Skip if the JSON file does not exist
            pass

def create_json_files():
    print("Create Json file")
    # Create the array with the required information for each open port
    for port in open_ports:
        data = {
            "ports": ports,
            "open": "open",
            "mac": mac_address
        }
        print(data)
        # Write the data to a JSON file named after the port number
        filename = f'{port}.json'
        print("trying to write date to : " + filename)
        with open(filename, 'w+') as f:
            json.dump(data, f, indent=4)
           # close(filename)

    # Create the array with the required information for each closed port
    for port in closed_ports:
        data = {
            "ports": ports,
            "open": "closed",
            "mac": mac_address
        }
        print(data)
        # Write the data to a JSON file named after the port number
        filename = f'{port}.json'
        with open(filename, 'w+') as f:
            json.dump(data, f, indent=4)
            #close(filename)


print("start")
# Check if nmap is installed
if not subprocess.run(["which", "nmap"], capture_output=True, text=True).stdout.strip():
    print("nmap is not installed, installing")
    subprocess.run(["sudo", "apt-get", "update"])
    subprocess.run(["sudo", "apt-get", "install", "-y", "nmap"])
for ports in ArrPorts:
    #port = str(ports)
# Get the IP address of the device
    ip_address = subprocess.check_output(["hostname", "-I"]).decode().strip()
    print(ip_address)
# Get the MAC address of the device
    mac_address = subprocess.check_output(["ip", "link", "show", "eth0"]).decode().splitlines()[1].split()[1]
    print(mac_address)
# Scan for open and closed ports
    result = subprocess.run(["sudo", "nmap","st", "-p", ports, ip_address], capture_output=True, text=True)
    print(result)
# Extract the list of open and closed ports
    open_ports = [line.split()[1] for line in result.stdout.splitlines() if "Ports:" in line]
    closed_ports = [line.split()[1] for line in result.stdout.splitlines() if "closed" in line and int(line.split("/")[0]) not in map(>
    print("ports")
    print(f"Open ports for {ip_address}: {', '.join(open_ports)}")
    print(f"MAC address of the device: {mac_address}")
    create_json_files()
Send_json()
print("create")
