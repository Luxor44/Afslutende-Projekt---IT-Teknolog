#!/usr/bin/env python3
import os
from flask import Flask, jsonify, request
import mysql.connector
from functools import wraps
import json

app = Flask(__name__)

SqlPassword = os.getenv('SqlPassword')
SqlUsername = os.getenv('SqlUsername')
BearerToken = os.getenv('BearerToken')
#BearerToken = "123"
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
# define the endpoint for database data
@app.route('/api/get/protocolscan', methods=['GET'])
@require_token
def get_protocolscan():
    # connect to database
    conn = mysql.connector.connect(
	host='localhost',
	user= SqlUsername,
	password= SqlPassword,
	database='Scanner'
    )
    c = conn.cursor()


    # get data from database

    c.execute('SELECT id, mac, protocol, unsecure FROM unsecure_protocols')
    rows = c.fetchall()


    # convert data to a list of dictionaries
    data = []
    for row in rows:
        data.append({
            'id': row[0],
            'mac': row[1],
            'protocol': row[2],
            'unsecure': row[3]
	})

    # get data as JSON
    return jsonify(data)


# define the endpoint for database data
@app.route('/api/get/portscan', methods=['GET'])
@require_token
def get_portscan():
    # connect to database
    conn = mysql.connector.connect(
	host='localhost',
	user= SqlUsername,
	password= SqlPassword,
	database='port_scanning'
    )
    c = conn.cursor()


    # get data from database

    c.execute('SELECT id, ports, open, mac FROM scanned_ports')
    rows = c.fetchall()


    # convert data to a list of dictionaries
    data = []
    for row in rows:
        data.append({
            'id': row[0],
            'ports': row[1],
            'open': row[2],
            'mac': row[3]
	})

    # get data as JSON
    return jsonify(data)


# define the endpoint to post JSON data to database
@app.route('/api/protocolscan', methods=['POST'])
@require_token
def post_data():
	# connect to database
	conn = mysql.connector.connect(
		host='localhost',
		user=SqlUsername,
		password=SqlPassword,
		database='Scanner'
	)
	c = conn.cursor()
    # Parse JSON data
	data = request.get_json()

    # insert data
	query = "INSERT INTO unsecure_protocols (mac, protocol, unsecure) VALUES (%s, %s, %s)"
	values = (data['mac'], data['protocol'], data['unsecure'])
	c.execute(query, values)
	conn.commit()

    # close database
	c.close()
	conn.close()

	return jsonify({'message': 'Data posed successfully'})

# define the endpoint to post JSON data to database
@app.route('/api/portscan', methods=['POST'])
@require_token
def post_datax():
    # connect to database
	conn = mysql.connector.connect(
		host='localhost',
		user=SqlUsername,
		password=SqlPassword,
		database='port_scanning'
	)
	c = conn.cursor()
    # Parse JSON data
	data = request.get_json()

    # insert data
	query = "INSERT INTO scanned_ports (ports, open, mac) VALUES (%s, %s, %s)"
	values = (data['ports'], data['open'], data['mac'])
	c.execute(query, values)
	conn.commit()

    # close database
	c.close()
	conn.close()

	return jsonify({'message': 'Data posed successfully'})

# API for login
@app.route('/api/Login', methods=['POST'])
@require_token
def get_login():
    # connect to database

	# username and password from request parameters
#	data = request.get_json()
#	Username = data['Username']
#	Password = data['Password']

	conn = mysql.connector.connect(
		host='localhost',
		user=SqlUsername,
		password=SqlPassword,
		database='Login'
	)
	c = conn.cursor()

	data = request.get_json()
	Username = data['Username']
	Password = data['Password']

    # get data from database
	query = "SELECT Number FROM Login WHERE Username = %s AND Password = %s"
	c.execute(query, (Username, Password))
    #c.execute('SELECT id, Username, Password, Number FROM Login')
	rows = c.fetchone()
	print(rows)
    # close database
	c.close()
	conn.close()

	data = json.dumps(rows)

    # get data as JSON
	return jsonify(data)
	#return jsonify({'message': 'Data posed successfully'})


if __name__=='__main__':
	app.run(host='192.168.8.163', port=5000)