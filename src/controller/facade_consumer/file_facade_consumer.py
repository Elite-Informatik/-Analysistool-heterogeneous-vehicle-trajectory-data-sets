from abc import ABC
from typing import Optional

from src.file.file_facade import FileFacade


class FileFacadeConsumer(ABC):
    """
    This abstract class defines the basic functionality for all classes that need to use the FileFacade.
    """

    def __init__(self):
        self._file_facade: Optional[FileFacade] = None

    @property
    def file_facade(self) -> FileFacade:
        """
        A property that returns the FileFacade instance.

        :raises: ValueError if the FileFacade has not been set yet.
        :return: an instance of the FileFacade class
        """
        if self._file_facade is None:
            raise ValueError("The file facade needs to be set before using {name}.".format(name=self.__str__()))
        return self._file_facade

    def set_file_facade(self, file_facade: FileFacade):
        """
        This method is used to set the FileFacade for the class.

        :param file_facade: an instance of the FileFacade class
        """
        self._file_facade = file_facade
