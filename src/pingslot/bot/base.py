from abc import ABC, abstractmethod


class Bot(ABC):
    def __init__(
        self,
    ):
        pass

    @abstractmethod
    async def init(
        self,
    ) -> None:
        pass

    @abstractmethod
    async def notify(self, message: str) -> None:
        pass

    @abstractmethod
    async def handle(
        self,
    ) -> None:
        pass
