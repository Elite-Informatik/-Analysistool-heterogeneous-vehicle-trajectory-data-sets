from abc import ABC
from typing import Optional

from src.database.dataset_facade import DatasetFacade


class DatasetFacadeConsumer(ABC):
    """
    This abstract class defines the basic functionality for all classes that need to use the DatasetFacade.
    """

    def __init__(self):
        self._dataset_facade: Optional[DatasetFacade] = None

    @property
    def dataset_facade(self) -> DatasetFacade:
        """
        A property that returns the DatasetFacade instance.

        :raises: ValueError if the DatasetFacade has not been set yet.
        :return: an instance of the DatasetFacade class
        """
        if self._dataset_facade is None:
            raise ValueError("The dataset facade needs to be set before using {name}.".format(name=self.__str__()))
        return self._dataset_facade

    def set_dataset_facade(self, dataset_facade: DatasetFacade):
        """
        This method is used to set the DatasetFacade for the class.

        :param dataset_facade: an instance of the DatasetFacade class
        """
        self._dataset_facade = dataset_facade
