import monobank

from .base import Base
from ..schemas import ProviderBase


class MonobankProvider(Base):

    @staticmethod
    def is_valid(data: ProviderBase) -> bool:
        token: str = data.api_key
        try:
            monobank.Client(token).get_client_info()
            return True
        except monobank.errors.Error:
            return False
