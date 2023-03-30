from abc import ABC
from abc import abstractmethod

from src.controller.output_handling.event import RefreshTrajectoryData


class TrajectoryEventConsumer(ABC):
    """
    An Interface that needs to be implemented by each class that should be able to process
    trajectory events. The implementations of the interface functions can be very different so
    the documentation is found in the implementation of classes that implement this interface.
    """

    @abstractmethod
    def process_refreshed_trajectory_data(self, event: RefreshTrajectoryData):
        """
        called whenever a RefreshTrajectoryData event was thrown
        """
        pass
