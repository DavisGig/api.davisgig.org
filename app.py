from flask import Flask, jsonify
from flask.ext.cors import CORS

app = Flask(__name__)
CORS(app, resources=r'/api/*', allow_headers='Content-Type')

@app.route('/api/')
def ping():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
