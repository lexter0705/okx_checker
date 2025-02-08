import abc


class ConnectCreator(abc.ABC):
    @abc.abstractmethod
    def create_connects(self, pairs: list[str]):
        pass