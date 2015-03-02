from flask import Flask, jsonify, request
from flask.ext.cors import CORS
from werkzeug.contrib.fixers import ProxyFix

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

    user = {
        'first':   data['first'],
        'last':    data['last'],
        'email':   data['email'],
        'ip_addr': request.remote_addr
    }

    db.contacts.insert(user)

    return jsonify({"success": True})

@app.route('/api/stats')
def stats():
    return jsonify({
        'contacts': db.contacts.count(),
        'households': len(db.contacts.distinct('ip_addr'))
    })

app.wsgi_app = ProxyFix(app.wsgi_app)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
