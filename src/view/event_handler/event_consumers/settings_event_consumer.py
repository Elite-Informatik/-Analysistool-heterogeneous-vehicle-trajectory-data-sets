from abc import ABC
from abc import abstractmethod

from src.controller.output_handling.event import SettingsChanged


class SettingsEventConsumer(ABC):
    """
    An Interface that needs to be implemented by each class that should be able to process
    setting events. The implementations of the interface functions can be very different so
    the documentation is found in the implementation of classes that implement this interface.
    """

    @abstractmethod
    def process_changed_settings(self, event: SettingsChanged):
        """
        called whenever an SettingsChanged event was thrown
        """
        pass
