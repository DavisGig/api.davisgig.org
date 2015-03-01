from flask import Flask, jsonify, request
from flask.ext.cors import CORS

app = Flask(__name__)
CORS(app, resources=r'/api/*', allow_headers='Content-Type')

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

    return jsonify({'user': {'first': first, 'last': last, 'email': email, 'ip_addr': ip_addr}})

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
