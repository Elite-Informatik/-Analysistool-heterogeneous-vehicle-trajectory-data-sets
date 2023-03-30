from abc import ABC
from abc import abstractmethod

from src.controller.output_handling.abstract_event import Event


class Distributor(ABC):
    """
    Each Event group has its own distributor. The distributor notifies the event consumers of that group
    about all events that are related to that group.
    """

    @abstractmethod
    def distribute_event(self, event: Event):
        """
        distributes the event to the subscribers
        :param event: the event
        """
        pass
