import os
from flask import Flask
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
app.config['CORS_HEADERS'] = 'Content-Type'

from flaskapp.routes import *

