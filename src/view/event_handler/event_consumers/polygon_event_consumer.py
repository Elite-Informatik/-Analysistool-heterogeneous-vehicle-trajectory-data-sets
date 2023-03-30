from abc import ABC
from abc import abstractmethod

from src.controller.output_handling.event import PolygonAdded
from src.controller.output_handling.event import PolygonChanged
from src.controller.output_handling.event import PolygonDeleted


class PolygonEventConsumer(ABC):
    """
    An Interface that needs to be implemented by each class that should be able to process
    polygon events. The implementations of the interface functions can be very different so
    the documentation is found in the implementation of classes that implement this interface.
    """

    @abstractmethod
    def process_added_polygon(self, event: PolygonAdded):
        """
        called whenever an PolygonAdded event was thrown
        """
        pass

    @abstractmethod
    def process_deleted_polygon(self, event: PolygonDeleted):
        """
        called whenever an PolygonDeleted event was thrown
        """
        pass

    @abstractmethod
    def process_changed_polygon(self, event: PolygonChanged):
        """
        called whenever an PolygonChanged event was thrown
        """
        pass
