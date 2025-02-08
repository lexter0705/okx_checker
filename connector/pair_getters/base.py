import abc


class PairGetter(abc.ABC):
    def __init__(self, link: str):
        self.__link = link

    @abc.abstractmethod
    def get_all_pairs(self) -> list[str]:
        pass

    @property
    def link(self) -> str:
        return self.__link