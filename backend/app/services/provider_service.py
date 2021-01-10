from ..schemas import ProviderBase
from ..providers.monobank import MonobankProvider

providers_classes = {
    "monobank": MonobankProvider,
}


class ProviderSerivce:
    def __init__(self, data: ProviderBase) -> None:
        self.data = data

    def get_provider(self):
        return providers_classes.get(self.data.name)
