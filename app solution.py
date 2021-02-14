from flask import Flask, jsonify, request
from flask_cors import CORS
from blockchain import Blockchain
from argparse import ArgumentParser
import requests

app = Flask(__name__)
CORS(app)


@app.route('/', methods=['GET'])
def chian():
    chain = test.chain
    dictChain = [block.__dict__.copy() for block in chain]
    for dictBlock in dictChain:
        dictBlock['transactions'] = [tx.__dict__ for tx in dictBlock['transactions']]
    return jsonify(dictChain), 200


@app.route('/mine', methods=['POST'])
def mine():
    block = test.addBlcok()
    if block != None:
        dictBlock = block.__dict__.copy()
        dictBlock['transactions'] = [tx.__dict__ for tx in dictBlock['transactions']]
        res = {
            'Block': dictBlock,
        }
        return jsonify(res), 201
    else:
        res = {
            'Error': 'Not able to mine a block',
        }
        return jsonify(res), 500


@app.route('/opentxs', methods=['GET'])
def opentxs():
    txs = test.unconfirmed
    if txs != None:
        dictTxs = [tx.__dict__ for tx in txs]
        res = {
            'transactions': dictTxs
        }
        return jsonify(res), 200
    else:
        res = {
            'Error': 'There is no a transaction',
        }
        return jsonify(res), 500


@app.route('/sendtx', methods=['POST'])
def sendtx():
    values = request.get_json()
    if not values:
        res = {
            'message': 'There is no input'
        }
        return jsonify(res), 400

    required = ['sender', 'receiver', 'amount']

    if not all(key in values for key in required):
        res = {
            'Message': 'missing a value'
        }
        return jsonify(res), 400

    sender = values['sender']
    receiver = values['receiver']
    amount = values['amount']
    passedTransaction = test.addTransaction(sender, receiver, amount)

    if passedTransaction != None:
        res = {'transaction': {
            'sender':  values['sender'],
            'receiver': values['receiver'],
            'amount': values['amount']
            }
        }
        return jsonify(res), 200
    else:
        res = {
            'Error': 'The transaction did not pass'
        }
        return jsonify(res), 500


if __name__ == '__main__':
    ser = ArgumentParser()
    ser.add_argument('-p', '--port', default=8020)
    args = ser.parse_args()
    port = args.port
    test = Blockchain()
    app.run(debug=True, port=port)
