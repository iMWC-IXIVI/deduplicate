class SizeValidator:
    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        return instance.__dict__.get(self.name, None)

    def __set__(self, instance, value):
        if value < 0:
            raise ValueError('Данное значение не поддерживается!!!')

        instance.__dict__[self.name] = value


class LuckValidator:
    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        return instance.__dict__.get(self.name, None)

    def __set__(self, instance, value):
        if not 0 < value < 1:
            raise ValueError('Данное значение не поддерживается!!!')

        instance.__dict__[self.name] = value
