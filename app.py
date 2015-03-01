from flask import Flask, jsonify, request
from flask.ext.cors import CORS

app = Flask(__name__)
CORS(app, resources=r'/api/*', allow_headers='Content-Type')

import os

host = os.environ['DB_PORT_27017_TCP_ADDR']
port = os.environ['DB_PORT_27017_TCP_PORT']

from pymongo import MongoClient

client = MongoClient(host, int(port))
db = client['davisgig']

@app.route('/api/')
def ping():
    return jsonify({"status": "ok"})

@app.route('/api/sign-up', methods=['POST'])
def sign_up():
    data = request.json

    first = data['first']
    last  = data['last']
    email = data['email']
    ip_addr = request.remote_addr

    db.contacts.insert({
        'first': first,
        'last': last,
        'email': email,
        'ip_addr': ip_addr})

    return jsonify({'user': {'first': first, 'last': last, 'email': email, 'ip_addr': ip_addr}})

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
