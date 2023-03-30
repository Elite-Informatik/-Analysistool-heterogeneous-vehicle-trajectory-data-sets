from typing import List

from src.controller.output_handling.abstract_event import Event
from src.controller.output_handling.event import DatasetAdded
from src.controller.output_handling.event import DatasetDeleted
from src.controller.output_handling.event import DatasetOpened
from src.view.event_handler.distributors.distributor import Distributor
from src.view.event_handler.event_consumers import DatasetEventConsumer


class DatasetEventDistributor(Distributor):
    """
    The DatasetEventDistributor notifies all its subscribers about dataset events.
    """

    def __init__(self):
        super().__init__()
        self._subscribers: List[DatasetEventConsumer] = []

    def distribute_event(self, event: Event):
        """
        Selects and the method to be called on the subscribers based on the event type
        :param event: the event
        """
        if type(event) == DatasetOpened:
            self._distribute_opened_dataset(event)
        elif type(event) == DatasetAdded:
            self._distribute_added_dataset(event)
        elif type(event) == DatasetDeleted:
            self._distribute_deleted_dataset(event)

    def subscribe(self, new_subscriber: DatasetEventConsumer):
        """
        The subscriber will be notified about future dataset events.
        :param new_subscriber: the new subscriber
        """
        self._subscribers.append(new_subscriber)

    def unsubscribe(self, subscriber: DatasetEventConsumer):
        """
        The subscriber will no longer be notified about future dataset events.
        :param subscriber: the subscriber
        """
        self._subscribers.remove(subscriber)

    def _distribute_deleted_dataset(self, event: DatasetDeleted):
        for subscriber in self._subscribers:
            subscriber.process_deleted_dataset(event)

    def _distribute_added_dataset(self, event: DatasetAdded):
        for subscriber in self._subscribers:
            subscriber.process_added_dataset(event)

    def _distribute_opened_dataset(self, event: DatasetOpened):
        for subscriber in self._subscribers:
            subscriber.process_opened_dataset(event)
