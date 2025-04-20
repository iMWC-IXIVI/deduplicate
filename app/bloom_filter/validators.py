class SizeValidator:
    """
    Класс дескриптор размера блум фильтра\n
    SizeValidator:\n
    attributes:
        name: str - Название атрибута класса, в котором вызывается дескриптор\n
    methods:
        __set_name__(self, owner: object, name: str) -> None - Создание атрибута класса, из которого вызывается дескриптор.
            arguments:
                owner: object - Класс, из которого вызывается дескриптор\n
                name: str - Название атрибута класса, из которого вызывается дескриптор\n
        __get__(self, instance: object, owner: object) -> Optional[int] - Возвращение значения атрибута
            arguments:
                instance: object - Экземпляр класса, из которого вызывается дескриптор\n
                owner: object - Класс, из которого вызывается дескриптор\n
        __set__(self, instance: object, value: int) -> None - Проверка и замена значения в атрибуте
            arguments:
                instance: object - Экземпляр класса, из которого вызывается дескриптор\n
                value: int - Значение, на которое будет меняться атрибут\n
    """
    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        return instance.__dict__.get(self.name, None)

    def __set__(self, instance, value):
        if value <= 0:
            raise ValueError('Значение size может быть только больше нуля!!!')

        instance.__dict__[self.name] = value


class LuckValidator:
    """
        Класс дескриптор вероятности ложного срабатывания блум фильтра\n
        LuckValidator:\n
        attributes:
            name: str - Название атрибута класса, в котором вызывается дескриптор\n
        methods:
            __set_name__(self, owner: object, name: str) -> None - Создание атрибута класса, из которого вызывается дескриптор.
                arguments:
                    owner: object - Класс, из которого вызывается дескриптор\n
                    name: str - Название атрибута класса, из которого вызывается дескриптор\n
            __get__(self, instance: object, owner: object) -> Optional[float] - Возвращение значения атрибута
                arguments:
                    instance: object - Экземпляр класса, из которого вызывается дескриптор\n
                    owner: object - Класс, из которого вызывается дескриптор\n
            __set__(self, instance: object, value: float) -> None - Проверка и замена значения в атрибуте
                arguments:
                    instance: object - Экземпляр класса, из которого вызывается дескриптор\n
                    value: float - Значение, на которое будет меняться атрибут\n
        """
    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        return instance.__dict__.get(self.name, None)

    def __set__(self, instance, value):
        if not 0 < value < 1:
            raise ValueError('Значение luck может быть в диапазоне от 0 до 1!!!')

        instance.__dict__[self.name] = value
