from typing import List

from src.controller.output_handling.abstract_event import Event
from src.controller.output_handling.event import SettingsChanged
from src.view.event_handler.distributors.distributor import Distributor
from src.view.event_handler.event_consumers import SettingsEventConsumer


class SettingsEventDistributor(Distributor):
    """
    The distributor that notifies all settings event consumers about settings related events.
    """

    def __init__(self):
        super().__init__()
        self._subscribers: List[SettingsEventConsumer] = []

    def distribute_event(self, event: Event):
        """
        distributes the event to the subscribers
        :param event: the event
        """
        if type(event) == SettingsChanged:
            self._distribute_settings_changed(event)

    def subscribe(self, new_subscriber: SettingsEventConsumer):
        """
        The subscriber will be notified about future settings events.
        :param new_subscriber: the new subscriber
        """
        self._subscribers.append(new_subscriber)

    def unsubscribe(self, subscriber: SettingsEventConsumer):
        """
        The subscriber will no longer be notified about future settings events.
        :param subscriber: the subscriber
        """
        self._subscribers.remove(subscriber)

    def _distribute_settings_changed(self, event: SettingsChanged):
        for subscriber in self._subscribers:
            subscriber.process_changed_settings(event)
