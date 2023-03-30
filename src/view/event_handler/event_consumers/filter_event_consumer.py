from abc import ABC
from abc import abstractmethod

from src.controller.output_handling.event import FilterAdded
from src.controller.output_handling.event import FilterChanged
from src.controller.output_handling.event import FilterComponentDeleted
from src.controller.output_handling.event import FilterGroupAdded
from src.controller.output_handling.event import FilterGroupChanged
from src.controller.output_handling.event import FilterMovedToGroup


class FilterEventConsumer(ABC):
    """
    An Interface that needs to be implemented by each class that should be able to process
    filters events. The implementations of the interface functions can be very different so
    the documentation is found in the implementation of classes that implement this interface.
    """

    @abstractmethod
    def process_added_filter(self, event: FilterAdded):
        """
        called whenever an FilterAdded event was thrown
        """
        pass

    @abstractmethod
    def process_deleted_filter(self, event: FilterComponentDeleted):
        """
        called whenever an FilterComponentDeleted event was thrown
        """
        pass

    @abstractmethod
    def process_changed_filter(self, event: FilterChanged):
        """
        called whenever an FilterChanged event was thrown
        """
        pass

    @abstractmethod
    def process_added_filter_group(self, event: FilterGroupAdded):
        """
        called whenever an FilterGroupAdded event was thrown
        """
        pass

    @abstractmethod
    def process_changed_filter_group(self, event: FilterGroupChanged):
        """
        called whenever an FilterGroupChanged event was thrown
        """
        pass

    @abstractmethod
    def process_moved_filter(self, event: FilterMovedToGroup):
        """
        called whenever an FilterMovedToGroup event was thrown
        """
        pass
