from abc import ABC
from abc import abstractmethod

from src.controller.output_handling.event import DatasetAdded
from src.controller.output_handling.event import DatasetDeleted
from src.controller.output_handling.event import DatasetOpened


class DatasetEventConsumer(ABC):
    """
    An Interface that needs to be implemented by each class that should be able to process
    dataset events. The implementations of the interface functions can be very different so
    the documentation is found in the implementation of classes that implement this interface.
    """

    @abstractmethod
    def process_added_dataset(self, event: DatasetAdded):
        """
        called whenever an DatasetAdded event was thrown
        """
        pass

    @abstractmethod
    def process_deleted_dataset(self, event: DatasetDeleted):
        """
        called whenever an DatasetDeleted event was thrown
        """
        pass

    @abstractmethod
    def process_opened_dataset(self, event: DatasetOpened):
        """
        called whenever an DatasetOpened event was thrown
        """
        pass
