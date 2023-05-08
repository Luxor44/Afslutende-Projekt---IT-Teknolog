import subprocess

# Check if nmap is installed
if not subprocess.run(["which", "nmap"], capture_output=True, text=True).stdout.strip():
    print("nmap is not installed, installing")
    subprocess.run(["sudo", "apt-get", "update"])
    subprocess.run(["sudo", "apt-get", "install", "-y", "nmap"])

# Get the IP address of the device
ip_address = subprocess.check_output(["hostname", "-I"]).decode().strip()

# Get the MAC address of the device
mac_address = subprocess.check_output(["ip", "link", "show", "eth0"]).decode().splitlines()[1].split()[1]

# Scan for open ports
result = subprocess.run(["sudo", "nmap", "-p-", "-T4", "-oG", "-", ip_address], capture_output=True, text=True)

# Extract the list of open ports
open_ports = [line.split()[1] for line in result.stdout.splitlines() if "Ports:" in line]

# Print the open ports and MAC address
print(f"Open ports for {ip_address}: {', '.join(open_ports)}")
print(f"MAC address of the device: {mac_address}")
