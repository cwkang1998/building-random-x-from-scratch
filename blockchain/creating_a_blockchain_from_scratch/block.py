from datetime import datetime
from hashlib import sha256


class Block:
    def __init__(self, height, data, previous_block_hash) -> None:
        self.height = height
        self.timestamp = datetime.utcnow()
        self.data = data
        self.previous_block_hash = previous_block_hash
        self.calculate_valid_hash()

    def __str__(self) -> str:
        return f'{self.height}:{self.data}:\t{self.timestamp}\t:{self.previous_block_hash}'

    # In the case for this POW blockchain
    # A consensus algo is used in mining in which
    # hashes generated must star with 4 0's
    # This is obviously different from bitcoin's
    # POW algo (a gross simplification)
    def is_hash_valid(self, hash: str) -> bool:
        return hash.startswith('0' * 4)

    def calculate_valid_hash(self):
        hash = ''
        nonce = 0

        print(f"Mining block {self.height}")

        while not self.is_hash_valid(hash):
            temp = str(self) + str(nonce)
            hash = sha256(temp.encode()).hexdigest()
            nonce += 1

        print(f"Successfully found hash {hash}")
        self.hash = hash
