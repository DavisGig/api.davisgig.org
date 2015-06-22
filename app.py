from flask import Flask, jsonify, request
from flask.ext.cors import CORS
from werkzeug.contrib.fixers import ProxyFix
import urllib
import urllib2

app = Flask(__name__)
CORS(app, resources=r'/api/*', allow_headers='Content-Type')

import sys
import os

host = os.environ['DB_PORT_27017_TCP_ADDR']
port = os.environ['DB_PORT_27017_TCP_PORT']
mailman_url = 'http://list.davisgig.org/mailman/subscribe/davisgig-announce'

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
        'first':   data['firstName'],
        'last':    data['lastName'],
        'email':   data['email'],
        'ip_addr': request.remote_addr
    }

    db.contacts.insert(user)
    urllib2.urlopen(urllib2.Request(mailman_url, urllib.urlencode({
        'email':    data['email'],
        'fullname': ' '.join([data['firstName'], data['lastName']]),
        'digest':   '0'
    })))

    return jsonify({"success": True})

@app.route('/api/stats')
def stats():
    return jsonify({
        'contacts': db.contacts.count(),
        'households': len(db.contacts.distinct('ip_addr'))
    })

app.wsgi_app = ProxyFix(app.wsgi_app)

if __name__ == "__main__":
    host_ip = '0.0.0.0'

    if len(sys.argv) == 2:
        host_ip = sys.argv[1]
    elif 'HOST_IP_ADDR' in os.environ:
        host_ip = os.environ['HOST_IP_ADDR']

    print('starting api server on {}'.format(host_ip))

    app.run(host=host_ip, debug=True)
