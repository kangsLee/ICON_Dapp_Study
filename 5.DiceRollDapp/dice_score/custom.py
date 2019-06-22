from iconservice import *


class RandomClass:
    def __init__(self, name: str, timestamp: int):
        self.name = name
        self.timestamp = timestamp

    def get_random(self):
        input_data = f'{self.timestamp}, {self.name}'.encode()
        hash = sha3_256(input_data)
        return int.from_bytes(hash, 'big') % 6