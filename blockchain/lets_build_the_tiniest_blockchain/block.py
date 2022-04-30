import hashlib as hasher


class Block:
    def __init__(self, index, timestamp, data, previous_hash) -> None:
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.hash_block()

    def hash_block(self) -> str:
        sha = hasher.sha256()
        sha.update(f'{self.index}{self.timestamp}{self.data}{self.previous_hash}'.encode())
        return sha.hexdigest()
