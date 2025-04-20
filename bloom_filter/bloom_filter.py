from hashlib import blake2s
from math import log, ceil

from bitarray import bitarray

from validators import SizeValidator, LuckValidator


class BloomFilter:
    size = SizeValidator()
    luck = LuckValidator()

    def __init__(self, size: int, luck: float):
        self.size = size
        self.luck = luck
        self.m = -((self.size * log(self.luck)) / (log(2) ** 2))
        self.k = (self.m / self.size) * log(2)
        self.array = bitarray(ceil(self.m))

    def add_item(self, data: str):
        for i in range(ceil(self.k)):
            index = self._get_index(data, i)
            self.array[index] = 1

    def _get_index(self, data: str, i: int):
        hash_value = blake2s((data + str(i)).encode()).digest()
        return int.from_bytes(hash_value, 'little') % ceil(self.m)

    def is_contains(self, data: str):
        for i in range(ceil(self.k)):
            index = self._get_index(data, i)
            if not self.array[index]:
                return False
        return True
