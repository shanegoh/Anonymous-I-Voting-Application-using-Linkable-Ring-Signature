import os
from flask import Flask
from web3 import Web3
from flask import Flask
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
app.config['CORS_HEADERS'] = 'Content-Type'
web3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))
#cors = CORS(app, resources={r"/events/edit/<id>": {"origins": "http://localhost:3000"}})

from flaskapp.routes import *

