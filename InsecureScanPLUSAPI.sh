#!/bin/bash -x
apiUrl="http://192.168.8.172:5000/api/protocolscan"
# Get IP address
get_ip_address() {
  ip=$(ifconfig | grep -Eo 'inet (addr:)?([0-9]*\.){3}[0-9]*' | grep -Eo '([0-9]*\.){3}[0-9]*' | grep -v '127.0.0.1')
  echo "$ip"
}
# puts ip into a variable
ip_address=$(get_ip_address)

# Define protocols in an array
ArrProtocols=("80" "443" "21" "23" "25" "110" "143" "53" "194" "119" "389" "161" "22")

# Initialize variables for each port (boolean)
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

# Puts the Ethernet MAC address into a variable called strMac
strMac=$(ip link show | awk '/ether/ {print $2}')
echo "$strMac"

# Check if OpenSSL is installed and if not then install
if ! command -v openssl &> /dev/null; then
  echo "openssl is not installed, installing..."
  sudo apt-get install openssl
fi

# Check if Nmap is installed and if not then install
if ! command -v nmap &> /dev/null; then
  echo "nmap is not installed, installing..."
  sudo apt-get install nmap -y
fi

# Check the SSL/TLS version and cipher suite
if command -v openssl &> /dev/null; then
  for protocol in "${ArrProtocols[@]}"; do
        echo "checks if the server support SSL/TSL"
    # Check if the server supports SSL/TLS
    if openssl s_client -connect "${ip_address}:${protocol}" -tls1_2 -cipher 'HIGH:!aNULL' 2>/dev/null | grep -q 'BEGIN CERTIFICATE'; then
                echo "SSL/TLS supported on port $protocol"

                echo "Checking for Heartbleed vulnerability..."
                if openssl s_client -connect "${ip_address}:${protocol}" -tlsextdebug -msg 2>/dev/null | grep 'heartbeat extension'; then
                        echo "Heartbleed vulnerability found on port $protocol"
                             data='{"mac":"$strMac","protocol":"$protocol","unsecure":true}'
                             #curl -X POST -H "Content-Type: application/json" "Authorization: $BearerToken" -d $data $apiUrl
                             curl -X POST --header "Content-Type: application/json" --header "Authorization: Bearer $BearerToken" -d "$data" "$apiUrl"
                        case $protocol in
                                "443") https_secure=false ;;
                                "80") http_secure=false ;;
                                "21") ftp_secure=false ;;
                                "23") telnet_secure=false ;;
                                "25") smtp_secure=false ;;
                                "110") pop3_secure=false ;;
                                "143") imap_secure=false ;;
                                "53") dns_secure=false ;;
                                "194") irc_secure=false ;;
                                "119") nntp_secure=false ;;
                                "389") ldap_secure=false ;;
                                "161") snmp_secure=false ;;
                                "22") ssh_secure=false ;;
                        esac
                else
                echo "&protocol has no HeartBleed vulnerability"
                     data='{"mac":"$strMac","protocol":"$protocol","unsecure":false}'
                     #curl -X POST -H "Content-Type: application/json" "Authorization: $BearerTokens" -d $data $apiUrl
                     curl -X POST --header "Content-Type: application/json" --header "Authorization: Bearer $BearerToken" -d "$data" "$apiUrl"
                fi
        fi
    if $(nmap -sT -p $protocol $ip_address | grep open >/dev/null); then
      echo "Vulnerability detected on port $protocol!"
      data='{"mac":"$strMac","protocol":"$protocol","unsecure":true}'
      #curl -X POST -H "Content-Type: application/json" "Authorization: $BearerTokens" -d $data $apiUrl
      curl -X POST --header "Content-Type: application/json" --header "Authorization: Bearer $BearerToken" -d "$data" "$apiUrl"
      case $protocol in
        "443") https_secure=false ;;
        "80") http_secure=false ;;
        "21") ftp_secure=false ;;
        "23") telnet_secure=false ;;
        "25") smtp_secure=false ;;
        "110") pop3_secure=false ;;
        "143") imap_secure=false ;;
        "53") dns_secure=false ;;
        "194") irc_secure=false ;;
        "119") nntp_secure=false ;;
        "389") ldap_secure=false ;;
        "161") snmp_secure=false ;;
        "22") ssh_secure=false ;;
      esac
        else
        echo "$protocol is secure"
        data='{"mac":"$strMac","protocol":"$protocol","unsecure":false}'
        #curl -X POST -H "Content-Type: application/json" "Authorization: $BearerTokens" -d $data $apiUrl
        curl -X POST --header "Content-Type: application/json" --header "Authorization: Bearer $BearerToken" -d "$data" "$apiUrl"
    fi
  done
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

#ifconfig | grep -Eo 'inet (addr:)?([0-9]*\.){3}[0-9]*' | grep -Eo '([0-9]*\.){3}[0-9]*' | grep -v '127.0.0.1'ifconfig | grep -Eo 'inet (addr:)?([0-9]*\.){3}[0-9]*' | grep -Eo '([0-9]*\.){3}[0-9]*' | grep -v '127.0.0.1'
