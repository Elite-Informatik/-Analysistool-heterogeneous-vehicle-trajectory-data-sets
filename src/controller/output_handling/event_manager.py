from abc import ABC
from abc import abstractmethod

from src.controller.facade_consumer import (EventHandlerConsumer)
from src.data_transfer.content.logger import logging


class IEventManager(ABC):
    """
    Interface for Eventmanager
    """

    def send_events(self, events: list) -> None:
        """
        Notifies all subscribed events handlers about multiple events.
        :param events: List of events to notify
        """
        pass

    @logging
    @abstractmethod
    def notify(self, events: list) -> None:
        """
        Notifies all subscribed events handlers about multiple events.
        :param events: List of events to notify
        """
        pass


class EventManager(IEventManager, EventHandlerConsumer):
    """
    EventManager is a class that manages the list of events handlers and notify the events to them.
    """

    def send_events(self, events: list) -> None:
        self.notify(events)

    def notify(self, events: list) -> None:

        for subscriber in self.event_handlers:
            for event in events:
                subscriber.notify_event(event)
