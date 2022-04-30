from datetime import datetime
import json
from typing import List
from flask import Flask
from flask import request

from block import Block

node = Flask(__name__)

blockchain: List[Block] = [Block(0, datetime.now(), {
    "proof-of-work": 9,
    "transactions": None
}, "0")]
# store node transactions
this_node_transaction = []

miner_address = 'q3nf394hjg-random-miner-address-34nf3i4nflkn3o'


def proof_of_work(last_proof):
    incrementor = last_proof + 1
    # keep incrementing until you find a number
    # divisible by 7. Thats the proof of work
    while not(incrementor % 7 == 0 and incrementor % last_proof == 0):
        incrementor += 1
    return incrementor


@node.route('/txion', methods=['POST'])
def transaction():
    if request.method == 'POST':
        new_txion = request.get_json()
        this_node_transaction.append(new_txion)

        print("New transaction")
        print(f"FROM: {new_txion['from']}")
        print(f"TO: {new_txion['to']}")
        print(f"AMOUNT: {new_txion['amount']}")

        return "Transaction submission successful"


@node.route('/mine', methods=['GET'])
def mine():
    last_block = blockchain[len(blockchain) - 1]
    last_proof = last_block.data['proof-of-work']

    # Find proof of work
    proof = proof_of_work(last_proof)
    this_node_transaction.append(
        {'from': 'network', 'to': miner_address, 'amount': 1}
    )
    new_block_data = {
        'proof-of-work': proof,
        'transactions': list(this_node_transaction)
    }
    new_block_index = last_block.index + 1
    new_block_timestamp = datetime.now()
    last_block_hash = last_block.hash
    this_node_transaction[:] = []

    # Create the new block
    mined_block = Block(
        new_block_index,
        new_block_timestamp,
        new_block_data,
        last_block_hash
    )
    blockchain.append(mined_block)
    return json.dumps({
        'index': new_block_index,
        'timestamp': str(new_block_timestamp),
        'data': new_block_data,
        'hash': last_block_hash
    }) + "\n"


@node.route('/blocks', methods=['GET'])
def get_blocks():
    return json.dumps([
        {'index': b.index,
         'timestamp': str(b.timestamp),
         'data': b.data,
         'hash': b.hash} for b in blockchain
    ])


node.run()
