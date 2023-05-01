#!/bin/bash

# Define Protocols in an Array
ArrProtocols=("http" "https" "ftp" "telnet" "smtp" "pop3" "imap" "dns" "irc" "nntp" "ldap" "snmp" "ssh")

# Initialize Variables for each port (bolean)
https_secure=true
http_secure=true
ftp_secure=true
telnet_secure=true
smtp_secure=true
pop3_secure=true
imap_secure=true
dns_secure=true
irc_secure=true
nntp_secure=true
ldap_secure=true
snmp_secure=true
ssh_secure=true
# puts the ethernets mac adress into a variable called strMac
strMac=$(ip link show | awk '/ether/ {print $2}')
echo $strMac
# Check if nmap is installed and if not then install
if ! command -v nmap &> /dev/null; then
    echo "nmap is not installed, installing..."
    sudo apt-get install nmap -y
fi

# Check procols if they are unsecure or not
if command -v nmap &> /dev/null; then
  for protocol in "${ArrProtocols[@]}"
  do
# -sT means we are using a TCP connect scan. -p defindes the ports or protocol
    if nmap -sT -p $protocol 127.0.0.1 | grep open > /dev/null; then
      case $protocol in
	"https") https_secure=false;;
        "http") http_secure=false;;
        "ftp") ftp_secure=false;;
        "telnet") telnet_secure=false;;
        "smtp") smtp_secure=false;;
        "pop3") pop3_secure=false;;
        "imap") imap_secure=false;;
        "dns") dns_secure=false;;
        "irc") irc_secure=false;;
        "nntp") nntp_secure=false;;
        "ldap") ldap_secure=false;;
        "snmp") snmp_secure=false;;
        "ssh") ssh_secure=false;;
      esac
    fi
  done
else
# exit
  exit 1
fi

# Output the results
echo "http_secure: $http_secure"
echo "ftp_secure: $ftp_secure"
echo "telnet_secure: $telnet_secure"
echo "smtp_secure: $smtp_secure"
echo "pop3_secure: $pop3_secure"
echo "imap_secure: $imap_secure"
echo "dns_secure: $dns_secure"
echo "irc_secure: $irc_secure"
echo "nntp_secure: $nntp_secure"
echo "ldap_secure: $ldap_secure"
echo "snmp_secure: $snmp_secure"
echo "ssh_secure: $ssh_secure"
