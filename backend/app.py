from flask import Flask, jsonify
from web3 import Web3


app = Flask(__name__)
web3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))

#@app.route("/")
#def hello():
#    return "Hello, World!"

# Declare Flask-Web3 extension
# web3 = FlaskWeb3(app=app)

@app.route("/transaction", methods = ['GET'])
def sendEth():
    web3.eth.send_transaction({
    'to': '0x713F1d2B79a25bA7055d42371245655495a209Ed',
    'from': '0xF8bd8f6C8a7a605F56cC4311aECB20Eea99daf5F',
    'value': '1000000000000000'
    })
    return "?"