# blockchain.py

import hashlib
import time
import json
from flask import Flask, request, jsonify

class Block:
    def __init__(self, index, previous_hash, timestamp, data, hash):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.hash = hash

def calculate_hash(index, previous_hash, timestamp, data):
    block_data = f'{index}{previous_hash}{timestamp}{data}'
    return hashlib.sha256(block_data.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block(0, '0', time.time(), 'Genesis Block', '0')
        self.chain.append(genesis_block)

    def add_block(self, data):
        index = len(self.chain)
        previous_hash = self.chain[-1].hash
        timestamp = time.time()
        hash = calculate_hash(index, previous_hash, timestamp, data)
        new_block = Block(index, previous_hash, timestamp, data, hash)
        self.chain.append(new_block)

app = Flask(__name__)
blockchain = Blockchain()

@app.route('/write_message', methods=['POST'])
def write_message():
    data = request.json.get('message')
    blockchain.add_block(data)
    response = {'message': 'Message added to the blockchain'}
    return jsonify(response), 201

@app.route('/get_messages', methods=['GET'])
def get_messages():
    messages = [block.data for block in blockchain.chain[1:]]
    response = {'messages': messages}
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(port=5000)
