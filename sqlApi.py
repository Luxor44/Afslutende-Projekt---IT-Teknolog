#!/usr/bin/env python3

from flask import Flask, jsonify, request
import mysql.connector

app = Flask(__name__)

# define the endpoint for database data
@app.route('/api')
def get_data():
    # connect to database
    conn = mysql.connector.connect(
	host='localhost',
	user='root',
	password='password',
	database='database'
    )
    c = conn.cursor()


    # get data from database

    c.execute('SELECT id, mac, protocol, unsecure FROM unsecure_protocols')
    rows = cursor.fetchall()


    # convert data to a list of dictionaries
    data = []
    for row in rows:
        data.apped({
            'id': row[0],
            'mac': row[1],
            'protocol': row[2],
            'unsecure': row[3]
	})

    # get data as JSON
    return jsonify(data)



# define the endpoint to post JSON data to database
@app.route('/api', methods=['POST'])
def post_data():
    # connect to database
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='password',
        database='database'
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

if __name__=='__main__':
    app.run()
