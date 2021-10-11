import hashlib
import json
from time import time
from typing import Dict, List, Set
from uuid import uuid4
from urllib.parse import urlparse

from flask import Flask, request
import requests


class Blockchain(object):
    def __init__(self):
        self.chain: List = []
        self.current_transactions: List = []
        self.nodes: Set = set()
        self.new_block(previous_hash=1, proof=100)

    def new_block(self, proof: int, previous_hash: str = None) -> Dict:
        block: Dict = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash_block(self.chain[-1]),
        }
        self.current_transactions = []
        self.chain.append(block)
        return block

    def new_transaction(self, sender: str, recipient: str, amount: int) -> int:
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })
        return self.last_block['index'] + 1

    @property
    def last_block(self) -> Dict:
        return self.chain[-1]

    @staticmethod
    def hash_block(block: Dict) -> str:
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def proof_of_work(self, last_proof: int) -> int:
        """
        Simple Proof of Work Algorithm:
         - Find a number p' such that hash(pp') contains leading 4 zeroes,
           where p is the previous p'
         - p is the previous proof, and p' is the new proof
        """
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1

        return proof

    @staticmethod
    def valid_proof(last_proof: int, proof: int) -> bool:
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == '0000'

    def register_node(self, address: str):
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)

    def valid_chain(self, chain: List) -> bool:
        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            print(f'{last_block}')
            print(f'{block}')
            print('\n-----------\n')
            if block['previous_hash'] != self.hash_block(last_block):
                return False

            if self.valid_proof(last_block['proof'], block['proof']):
                return False
            last_block = block
            current_index += 1
        return True

    def resolve_conflicts(self):
        neighbours = self.nodes
        new_chain = None
        max_length = len(self.chain)

        for node in neighbours:
            response = requests.get(f'http://{node}/chain')

            if response.status_code == 200:
                length, chain = response.json()

                if (length > max_length) and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain

        if new_chain:
            self.chain = new_chain
            return True

        return False


app = Flask(__name__)

node_identifier = str(uuid4()).replace('-', '')

blockchain = Blockchain()


@app.route('/mine', methods=['GET'])
def mine():
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)

    blockchain.new_transaction(
        sender="0", recipient=node_identifier, amount=1,)

    previous_hash = blockchain.hash_block(last_block)
    block = blockchain.new_block(proof, previous_hash)

    response = {'message': 'New block forged',
                'index': block['index'],
                'transactions': block['transactions'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash']}
    return response, 200


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()
    required = ['sender', 'recipient', 'amount']
    if values is None or not all(k in values for k in required):
        return {'message': 'Missing values'}, 400

    index = blockchain.new_transaction(**values)
    response = {'message': f'Transaction will be added to Block {index}'}
    return response, 201


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
    }
    return response, 200


@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    values = request.get_json()
    nodes = values.get('nodes')

    if nodes is None:
        return {'message': 'Please supply a valid list of nodes'}, 400

    for node in nodes:
        blockchain.register_nodes(node)

    response = {'message': 'New nodes have been added',
                'total_nodes': list(blockchain.nodes), }

    return response, 201


@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = blockchain.resolve_conflicts()
    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': blockchain.chain
        }
    else:
        response = {
            'message': 'Out chain is authoritative',
            'chain': blockchain.chain
        }
    return response, 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
