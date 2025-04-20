import json

from hashlib import blake2s
from math import log, ceil

from bitarray import bitarray

from .validators import SizeValidator, LuckValidator


class BloomFilter:
    """
    Класс реализация Filter Blooms\n
    BloomFilter:\n
    class_attributes:
        size: SizeValidator - Количество элементов в массиве\n
        luck: LuckValidator - Вероятность ложного срабатывания
    __attributes:
        __bits: int - Счётчик занятых битов
    attributes:
        m: float - Объем данных\n
        k: float - Количество хэш-функций\n
        array: bitarray - Bit массив
    methods:
        _get_index(self, data: dict, i: int) -> int - Получение индекса массива\n
        (static) get_data (data: dict) -> str - Создание хэш данных\n
        add_item(self. data: dict) -> None - Добавление 1-иц в массив\n
        is_contains(self, data: dict) -> bool - Проверка на принадлежность данных к массиву\n
        reset_array(self) -> None - Очищение массива данных
    """
    size = SizeValidator()
    luck = LuckValidator()

    def __init__(self, size: int, luck: float):
        self.size = size
        self.luck = luck
        self.m = -((self.size * log(self.luck)) / (log(2) ** 2))
        self.k = (self.m / self.size) * log(2)
        self.array = bitarray(ceil(self.m))
        self.__bits = 0

    def add_item(self, data: dict):
        data = self._get_data(data)

        for i in range(ceil(self.k)):
            index = self._get_index(data, i)
            if not self.array[index]:
                self.array[index] = 1
                self.__bits += 1

        if self.__bits / ceil(self.m) > 0.8:
            self.reset_array()

    def is_contains(self, data: dict):
        data = self._get_data(data)

        for i in range(ceil(self.k)):
            index = self._get_index(data, i)

            if not self.array[index]:
                return False

        return True

    def reset_array(self):
        self.array = bitarray(ceil(self.m))
        self.__bits = 0

    def _get_index(self, data: str, i: int):
        hash_value = blake2s((data + str(i)).encode()).digest()
        return int.from_bytes(hash_value, 'little') % ceil(self.m)

    @staticmethod
    def _get_data(data: dict):
        return json.dumps(data, sort_keys=True)
