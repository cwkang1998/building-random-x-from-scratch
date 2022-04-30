import datetime
from block import Block


def create_genesis_block():
    return Block(0, datetime.datetime.now(), "Genesis block", "0")
