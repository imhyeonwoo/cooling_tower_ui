# -*- coding: utf-8 -*-
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return '<h1>Cooling Tower Monitor</h1><p>Server is running!</p>'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
