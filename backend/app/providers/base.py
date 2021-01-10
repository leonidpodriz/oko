from ..schemas import ProviderBase


class Base:

    def __init__(self, data: ProviderBase) -> None:
        self.__is_valid(data)
        self.data = data

    @classmethod
    def __is_valid(cls, data: ProviderBase, raise_exeption: bool = True) -> bool:
        if cls.is_valid(data):
            return True

        if raise_exeption:
            raise Exception("Provider is not valid")

        return False

    @staticmethod
    def is_valid(data: ProviderBase) -> bool:
        return False
