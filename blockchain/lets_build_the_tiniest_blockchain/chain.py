from genesis import create_genesis_block
from new_block import next_block

# Create the blockchain
blockchain = [create_genesis_block()]
previous_block = blockchain[0]

# Add some blocks to the chain
num_blocks_to_add = 20

for i in range(num_blocks_to_add):
    blocks_to_add = next_block(previous_block)
    blockchain.append(blocks_to_add)
    previous_block = blocks_to_add

    # Broadcast
    print(f'Block #{blocks_to_add.index} has been added to the blockchain.')
    print(f'Hash: {blocks_to_add.hash}')
