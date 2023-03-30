from abc import ABC
from abc import abstractmethod

from src.controller.output_handling.abstract_event import Event


class IEventHandlerNotify(ABC):
    """
    This interface defines the methods that are public to components that send events to the events handler and
    want to notify the view about events. You can imagen this interface like the front of the events handler that
    is seen by view external components.
    """

    @abstractmethod
    def notify_event(self, event: Event):
        """
        Sends an event to the view. The eventhandler passes the event on to the view elements.
        The view Elements then process the event and update them self.

        :param event: the event that should be processed by the view
        """
        pass
