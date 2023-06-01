# Imports
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import numpy as np
from flask import Flask, render_template, url_for, session, request, jsonify
from io import BytesIO
import base64
import mysql.connector
import requests
import hashlib
import random
import json
from functools import wraps
import vonage
import string
import os


# Tomme variabler
ip_address = ""
mac_address = ""
ssltsl = ""
Heartbleed = ""
protocols = ""
id = ""

Protocoldata = []
Portdata = []

#Phone_number = None


app = Flask(__name__)

random_string = ""

BearerToken = os.getenv('BearerToken')
vonageKey = os.getenv('vonageKey')
vonageSecret = os.getenv('vonageSecret')


app.secret_key = "grp7"

# Vaelg data der skal overfoeres
url = "http://192.168.0.182:5000/api/get/protocolscan"
def get_api_data():
    headers = {"Authorization": "Bearer "+BearerToken, "Content-Type": "application/json"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        Protocoldata = response.json()
        print(Protocoldata)

       # Protocoldata = json.loads(Protocoldata)
        return Protocoldata
    else:
        print('Error: Unable to retrieve data from API')
        return None

# Hent Portdata
port_url = "http://192.168.0.182:5000/api/get/portscan"
def port_get_api_data():
    headers = {"Authorization": "Bearer "+BearerToken, "Content-Type": "application/json"}
    response = requests.get(port_url, headers=headers)
    if response.status_code == 200:
        Portdata = response.json()
        print(Portdata)
       # Protocoldata = json.loads(Protocoldata)
        return Portdata
    else:
        print('Error: Unable to retrieve data from API')
        return None


#Portdata = port_get_api_data()


# MatPlotLib
def matPlotsTemp():
#    global Portdata
   # Portdata = port_get_api_data()
    MacAdress = []
    port_counts = {}
    plotdata = {}
    result_dict = {}
"""
# Insert i dictionary
    desired_dict = None

    for item in Protocoldata:
        if 'SSLTSL' in item:
            desired_dict = item
            break

    if desired_dict:
        ssltsl_value = desired_dict['SSLTSL']
        new_dict = {}

        for pair in ssltsl_value.split(','):
            key, value = pair.split(':')
            new_dict[key.strip()] = value.strip()

        print("-------------HERUNDER-----------------------")
        for key, value in new_dict.items():
            print(key + ':', value)
            print("------------------------------------")

"""

    for i in Portdata:
        #MacAdress.append(i['MacAdress'])
        #plotdata[i['MacAdress']] = count_open_ports

        count_open_ports = i["Ports"].count("open")
        plotdata[i['MacAdress']] = count_open_ports

        print("------------------------------------")


        for x in Protocoldata:
            if i['MacAdress'] == x['MacAdress']:

                #count_open_ports = i["Ports"].count("open")
                print("Ports", count_open_ports)
                count_ssltsl = x["SSLTSL"].count("Certificate not found")
                print("SSL", count_ssltsl)
                count_heartbleed = x["HeartBleedVulnability"].count("vulnerable")
                print("Heatbleed", count_heartbleed)
                count_protocol = x["Protocols"].count("open")
                print("Protocol",  count_protocol)
                count_total = count_open_ports + count_ssltsl + count_heartbleed + count_protocol
                plotdata[i['MacAdress']] = count_total 

            elif i['MacAdress'] != x['MacAdress']:
                plotdata[i['MacAdress']] = count_open_ports 
 

            
                #count_open_ports = i["Ports"].count("open")
                count_ssltsl = x["SSLTSL"].count("Certificate not found")
                count_heartbleed = x["HeartBleedVulnability"].count("vulnerable")
                count_protocol = x["Protocols"].count("open")

                count_protocol_data = count_ssltsl + count_heartbleed + count_protocol
                plotdata[x['MacAdress']] = count_protocol_data
#                plotdata[i['MacAdress']] = count_open_ports 

       # plotdata[i['MacAdress']] = count_total


    x = list(plotdata.keys())
    y = list(plotdata.values())

    fig = Figure()
    ax = fig.subplots()
    ax.xaxis.label.set_color('black') #setting up X-axis label color to hotpink
    ax.yaxis.label.set_color('black') #setting up Y-axis label color to hotpink

    x = np.array(x)
    y = np.array(y)

#    ax.plot(x, y, linestyle = 'solid', c= '#20C20E', linewidth = '2', 
#    marker = 'o', mec = '#20C20E', ms = 5, mfc = 'white')

    ax.bar(x, y, color='#20C20E', width = 0.3)
    fig.patch.set_facecolor('#222') # outer plot background color HTML white
    ax.set_facecolor("#222") #inner plot background
    ax.tick_params(axis='x', colors='#fff') #setting up X-axis tick color to black
    ax.tick_params(axis='y', colors='#fff') #farve på skrift
    ax.set_title(mac_address, color='#fff') #-#-#
    for axis in ['top', 'bottom', 'left', 'right']: #bestemmer rammen er hvid 
        ax.spines[axis].set_color('#fff') 
    plt.figure(figsize=(1,4))
    plt.bar(x, y)
    buf = BytesIO()
    fig.savefig(buf, format="png")
    plot1 = base64.b64encode(buf.getbuffer()).decode("ascii")
    return plot1





# Service meddelse ifb. med login
fail_msg = "" 


# Startsiden til login og videreføring til Dashboard, hvis logget ind
@app.route('/', methods = ['GET','POST'])
def login():
    global Portdata
    global Protocoldata
    global Phone_number
    fail_msg = ""
    if session.get('loggedin') == None and session.get('1fa') == None:
        #Tjek brugernavn og kode, via db
        if request.method == 'POST':
            h = hashlib.sha256()
            Username = request.form['username']
            Password = request.form['password']
            url = "http://192.168.0.182:5000/api/Login"
            Password = Password.encode('utf-8')
            Password = h.update(Password)
            Password = h.hexdigest()
            print(Password)

            headers = {"Authorization": "Bearer "+BearerToken, "Content-Type": "application/json"}
            payload = {"Username": Username, "Password": Password}

            response = requests.post(url, headers=headers, data=json.dumps(payload))
            print(response.text)

            if response.status_code == 200: #Hvis statuskode er korrekt
                    print("Request succeeded")
                    user = response.json()
                    print(user)
                    user_list = json.loads(user)
                    Phone_number = user_list[0]
                    #print(Phone_number)
                    session['username']= Username
                    session['1fa']= True
                    session['loggedin']= None
                    etfa = True
                    global random_string
                    print("test"+Phone_number)
                    random_string = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

                    #change the key string and secret string to the os.getenv vonageKey and vonageSecret
                    client = vonage.Client(key= vonageKey, secret= vonageSecret)
                    sms = vonage.Sms(client)
                    #global Phone_number
                    responseData = sms.send_message(
                       {
                        "from": "Vonage APIs",
                        "to": "45" + Phone_number,
                        "text": "Your MFA code is: " + random_string,
                       }
                    )

                    if responseData["messages"][0]["status"] == "0":
                        print("Message sent successfully.")
                        return render_template('login.html', etfa=etfa)
                    else:
                        print(f"Message failed with error: {responseData['messages'][0]['error-text']}")
                        #return render_template('login.html', etfa=etfa)

            else:
                print("Wrong username or password")
                fail_msg = "Username or password is incorrect"
                return render_template('login.html', fail_msg=fail_msg)



# Check 2fa
    elif session.get('loggedin') == None and session.get('1fa') == True:
        tofa = request.form['2fa']

        if tofa == random_string:
            session['loggedin'] = True
            plot1 = matPlotsTemp()
            if not Protocoldata or not Portdata:
                Protocoldata = get_api_data()
                Portdata = port_get_api_data()
            return render_template("dashboard.html", Username=session['username'], loggedin=session['loggedin'], plot1=plot1, Protocoldata=Protocoldata, Portdata = Portdata)
        else:
            session['1fa']= None
            fail_msg="Incorrect code, please sign in again"
            return render_template('login.html', fail_msg=fail_msg)


# Hvis du allerede er logget ind ---------------------------------------------------------------------------------------------------------------------------------------------------------------
    elif session.get('loggedin') == True:

# If Protocoldata is None or Portdata is None:
        if not Protocoldata or not Portdata:
            Protocoldata = get_api_data()
            Portdata = port_get_api_data()
        plot1 = matPlotsTemp()

# Afslutning
        return render_template("dashboard.html", Username=session['username'], plot1 = plot1, Protocoldata=Protocoldata, Portdata = Portdata)
    return render_template("login.html")


# ------------------------------------------------------------------------------------------------------------------------------------------------------

# Logout
@app.route('/logout')
def logout():
    session.clear()
    msg_logout = 'You signed out!'
    return render_template('login.html', msg_logout=msg_logout)

# Session Cheat
@app.route('/cheat')
def cheat():
    session['username'] = 'admin'
    session['loggedin'] = True
    return render_template('login.html', Username=session['username'], loggedin=session['loggedin'])

# Kører shittet
if __name__ == "__main__":
    app.run(debug=True)
