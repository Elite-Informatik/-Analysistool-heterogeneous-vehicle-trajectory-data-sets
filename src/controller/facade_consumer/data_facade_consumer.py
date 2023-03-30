from abc import ABC
from typing import Optional

from src.database.data_facade import DataFacade


class DataFacadeConsumer(ABC):
    """
    This abstract class defines the basic functionality for all classes that need to use the DataFacade.
    """

    def __init__(self):
        self._data_facade: Optional[DataFacade] = None

    @property
    def data_facade(self) -> DataFacade:
        """
        A property that returns the DataFacade instance.

        :raises: ValueError if the DataFacade has not been set yet.
        :return: an instance of the DataFacade class
        """
        if self._data_facade is None:
            raise ValueError("The data facade needs to be set before using {name}.".format(name=self.__str__()))
        return self._data_facade

    def set_data_facade(self, data_facade: DataFacade):
        """
        This method is used to set the DataFacade for the class.

        :param data_facade: an instance of the DataFacade class
        """
        self._data_facade = data_facade
