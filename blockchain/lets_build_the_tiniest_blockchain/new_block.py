import datetime
from block import Block


def next_block(last_block: Block) -> Block:
    this_index = last_block.index + 1
    this_timestamp = datetime.datetime.now()
    this_data = f"Hey, I'm block {this_index}"
    this_hash = last_block.hash
    return Block(this_index, this_timestamp, this_data, this_hash)
