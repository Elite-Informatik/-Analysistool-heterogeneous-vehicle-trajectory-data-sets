from abc import ABC
from abc import abstractmethod


class FileRecord(ABC):
    """
    represents a file
    """

    @abstractmethod
    def save(self, path: str) -> None:
        """
        saves itself on the given path
        :param path:    the given path
        """
        pass
