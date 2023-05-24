#!/usr/bin/env python3
import os
from flask import Flask, jsonify, request
import mysql.connector
from mysql.connector import pooling
from functools import wraps
import json

app = Flask(__name__)

SqlPassword = os.getenv('SqlPassword')
SqlUsername = os.getenv('SqlUsername')
BearerToken = os.getenv('BearerToken')


#Create SQL poooling connection
sqlPool = pooling.MySQLConnectionPool(
    pool_name="MasterDatabasePool",
    pool_size=10,
    host="localhost",
    database="MasterDatabase",
    user=SqlUsername,
    password=SqlPassword

)
# Define a function to execute queries
def execute_query(query, values=None, fetch="all"):
    # Get a connection from the pool
    conn = sqlPool.get_connection()

    # Execute the query
    c = conn.cursor()
    c.execute(query, values)

    # Determine fetch type and return the results
    if fetch == "all":
        results = c.fetchall()
    elif fetch == "one":
        results = c.fetchone()

    # Commit the changes and release the connection
    conn.commit()
    conn.close()

    return results

# def Authorization
def require_token(func):
        @wraps(func)
        def decorated(*args, **kwargs):
                Token = None
                if 'Authorization' in request.headers:
                        auth_header = request.headers['Authorization']
                        Token = auth_header.split(" ")[1]
                if not Token:
                        return jsonify({'message': 'Token is missing'}), 401
                if Token != BearerToken:
                        return jsonify({'message': 'Token is invalid'}), 401
                return func(*args, **kwargs)
        return decorated

# define get data from protocolscan
@app.route('/api/get/protocolscan', methods=['GET'])
@require_token
def get_protocolscan():
        query = 'SELECT t1.* FROM ProtocolScan t1 LEFT JOIN ProtocolScan t2 ON t1.MacAdress = t2.MacAdress AND t1.Datetime < t2.Datetime WHERE t2.Datetime IS NULL'

        rows = execute_query(query, fetch="all")
    # convert data to a list of dictionaries
        data = []
        for row in rows:
                data.append({
                        'id': row[0],
                        'IpAdress': row[1],
                        'MacAdress': row[2],
                        'SSLTSL': row[3],
                        'HeartBleedVulnability': row[4],
                        'Protocols': row[5],
                        'Datetime': row[6]
        })

    # get data as JSON
        return jsonify(data)


# define get data from portscan
@app.route('/api/get/portscan', methods=['GET'])
@require_token
def get_portscan():
  # get data from database
    query = 'SELECT t1.* FROM PortScan t1 LEFT JOIN PortScan t2 ON t1.MacAdress = t2.MacAdress AND t1.Datetime < t2.Datetime WHERE t2.Datetime IS NULL'
    rows = execute_query(query, fetch="all")

    # convert data to a list of dictionaries
    data = []
    for row in rows:
        data.append({
            'id': row[0],
            'IpAdress': row[1],
            'MacAdress': row[2],
            'Ports': row[3],
            'Datetime': row[4]
        })

    # get data as JSON
    return jsonify(data)


# define post data to protocolscan
@app.route('/api/protocolscan', methods=['POST'])
@require_token
def post_protocol():
    # Parse JSON data
        data = request.get_json()
     # in order to post a dictionary to our mysql database we need to json.dump the data
        protocols_json = json.dumps(data['Protocols'])
        SSLTSL_json = json.dumps(data['SSLTSL'])
        HeartBleedVulnability_json = json.dumps(data['HeartBleedVulnability'])

    # insert data
        query = "INSERT INTO ProtocolScan (IpAdress, MacAdress, SSLTSL, HeartBleedVulnability, Protocols) VALUES (%s, %s, %s, %s, %s)"
        values = (data['IpAdress'], data['MacAdress'],SSLTSL_json, HeartBleedVulnability_json, protocols_json)
        execute_query(query, values)
        return jsonify({'message': 'Data posted successfully'})

# define the endpoint to post JSON data to database
@app.route('/api/portscan', methods=['POST'])
@require_token
def post_ports():
    # Parse JSON data
        data = request.get_json()
     # in order to post a dictionary to our mysql database we need to json.dump the data
        ports_json = json.dumps(data['Ports'])

    # Make query
        query = "INSERT INTO PortScan (IpAdress, MacAdress, Ports) VALUES (%s, %s, %s)"
    # Define values
        values = (data['IpAdress'], data['MacAdress'], ports_json)
    # call our execute_query function with query and values
        execute_query(query, values)

        return jsonify({'message': 'Data posted successfully'})
# API to Post a new user into database
@app.route('/api/add/user', methods=['POST'])
@require_token
def add_user():
    data = request.get_json()
    username = data['username']
    password = data['password']
    phonenumber = data['phonenumber']
    
    query = "INSERT INTO login (username, password, phonenumber) VALUES (%s, %s, %s)"
    values = (username, password, phonenumber)
    
    execute_query(query, values)
    
    return jsonify({'message': 'Data posted successfully'})
# API for login
@app.route('/api/Login', methods=['POST'])
@require_token
def get_login():
    # Parse JSON Data
        data = request.get_json()
    # make variables for data recieved
        Username = data['Username']
        Password = data['Password']
     # make a list of the data recieved
        values = (Username, Password)
    # get data from database
        query = "SELECT phonenumber FROM login WHERE username = %s AND password = %s"
        rows = execute_query(query, values, fetch="one")
    # return data
        data = json.dumps(rows)

    # get data as JSON
        return jsonify(data)



if __name__=='__main__':
        app.run(host='192.168.8.174', port=5000)
