from typing import List
from block import Block


class Blockchain:
    def __init__(self) -> None:
        self.blocks: List[Block] = []
        self.set_genesis_block()

    def set_genesis_block(self):
        data = 'Genesis'
        prev_hash = '0' * 64
        genesis_block = Block(0, data, prev_hash)
        self.blocks.append(genesis_block)

    def get_last_hash(self):
        last_block = self.blocks[-1]
        return last_block.hash

    def add_new_block(self, data):
        last_hash = self.get_last_hash()
        new_block = Block(len(self.blocks), data, last_hash)
        self.blocks.append(new_block)
