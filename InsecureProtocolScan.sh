#!/bin/bash -x
apiUrl="http://192.168.8.174:5000/api/protocolscan"
# Get IP address
get_ip_address() {
  ip=$(ifconfig | grep -Eo 'inet (addr:)?([0-9]*\.){3}[0-9]*' | grep -Eo '([0-9]*\.){3}[0-9]*' | grep -v '127.0.0.1')
  echo "$ip"
}
# puts ip into a variable
ip_address=$(get_ip_address)

# Define protocols in an array
ArrProtocols=("80" "443" "21" "23" "25" "110" "143" "53" "194" "119" "389" "161" "22")
# Define dictionaries

declare -A dict_SSLTLS
declare -A dict_HeartBleed
declare -A dict_Protocol

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
                                SSLTLS_Status="Certificate found"
                                echo "Checking for Heartbleed vulnerability..."
                if openssl s_client -connect "${ip_address}:${protocol}" -tlsextdebug -msg 2>/dev/null | grep 'heartbeat extension'; then
                        echo "Heartbleed vulnerability found on port $protocol"
                                                strHeartbleed="vulnerable"

                else
                        echo "protocol has no HeartBleed vulnerability"

                fi
        fi

        if $(nmap -sT -p $protocol $ip_address | grep open >/dev/null); then
                strProtocolStatus="open"
    fi
        dict_SSLTLS[$protocol]=$SSLTLS_Status
        dict_Heartbleed[$protocol]=$strHeartbleed
        dict_Protocol[$protocol]=$strProtocolStatus
  done
fi
data="{\"IpAdress\": \"$ip_address\",\"MacAdress\": \"$strMac\",\"SSLTSL\":{"
for key in "${!dict_SSLTLS[@]}"; do
        value="${dict_SSLTLS[@]}"
        if [[ value != "Certificate found" ]]; then
                value="Certificate not found"
        fi
        data+="\"$key\":\"$value\","
done
data="${data%,} }"
data+=", \"HeartBleedVulnability\": {"
for key in "${!dict_Heartbleed[@]}"; do
        value="${dict_Heartbleed[@]}"
        if [[ value != "vulnerable" ]]; then
                value="Secure"
        fi
        data+="\"$key\":\"$value\","
done
data="${data%,} }"
data+=", \"Protocols\": {"

for key in "${!dict_Protocol[@]}"; do
        value="${dict_Protocol[@]}"
        if [[ value != "open" ]]; then
                value="closed"
        fi
        data+="\"$key\":\"$value\","
done
data="${data%,} }"
data+="}"
echo "$data"
curl -X POST -H "Content-Type: application/json" "Authorization: $BearerTokens" -d $data $apiUrl
curl -X POST --header "Content-Type: application/json" --header "Authorization: Bearer $BearerToken" -d "$data" "$apiUrl"
