import subprocess
import json

def create_json_files():
    # Get the open and closed ports and MAC address
    result = subprocess.run(['sudo', 'nmap', '-sS', '-p', '1-65535', 'localhost'], capture_output=True, text=True)
    open_ports = [line.split()[1] for line in result.stdout.splitlines() if "open" in line]
    closed_ports = [str(port) for port in range(1, 65536) if str(port) not in open_ports]
    mac_address = subprocess.check_output(["ip", "link", "show", "eth0"]).decode().splitlines()[1].split()[1]

    # Create the array with the required information for each open port
    for port in open_ports:
        data = {
            'port_number': port,
            'mac_address': mac_address,
            'status': 'open'
        }
        # Write the data to a JSON file named after the port number
        filename = f'{port}.json'
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)

    # Create the array with the required information for each closed port
    for port in closed_ports:
        data = {
            'port_number': port,
            'mac_address': mac_address,
            'status': 'closed'
        }
        # Write the data to a JSON file named after the port number
        filename = f'{port}.json'
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)

    # If no open ports were found, print a message
    if not open_ports:
        print("No open ports found")

create_json_files()
