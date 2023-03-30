from abc import ABC
from typing import List

from src.view.event_handler.event_handler import IEventHandlerNotify


class EventHandlerConsumer(ABC):
    """
    This abstract class defines the basic functionality for all classes that need to use the EventHandler.
    """

    def __init__(self):
        """
        Initializes an empty list of events handlers
        """
        self.event_handlers: List[IEventHandlerNotify] = list()

    def subscribe(self, event_handler: IEventHandlerNotify) -> None:
        """
        Allows an events handler to subscribe to notifications.
        :raise ValueError: if event handler is none
        :param event_handler: EventHandler object to subscribe
        """
        if event_handler is None:
            raise ValueError("Can only use event handlers from None list.")
        self.event_handlers.append(event_handler)

    def unsubscribe(self, event_handler: IEventHandlerNotify) -> None:
        """
        Allows an events handler to unsubscribe from notifications.
        :param event_handler: EventHandler object to unsubscribe
        """
        self.event_handlers.remove(event_handler)
