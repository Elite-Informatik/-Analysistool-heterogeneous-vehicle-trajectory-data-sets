from typing import List

from src.controller.output_handling.abstract_event import Event
from src.controller.output_handling.event import PolygonAdded
from src.controller.output_handling.event import PolygonChanged
from src.controller.output_handling.event import PolygonDeleted
from src.view.event_handler.distributors.distributor import Distributor
from src.view.event_handler.event_consumers import PolygonEventConsumer


class PolygonEventDistributor(Distributor):
    """
    The distributor that notifies the polygon event consumers about polygon related events.
    """

    def __init__(self):
        super().__init__()
        self._subscribers: List[PolygonEventConsumer] = []

    def distribute_event(self, event: Event):
        """
        distributes the event to the subscribers
        :param event: the event
        """
        if type(event) == PolygonAdded:
            self._distribute_polygon_added(event)
        elif type(event) == PolygonDeleted:
            self._distribute_polygon_deleted(event)
        elif type(event) == PolygonChanged:
            self._distribute_changed_polygon(event)

    def subscribe(self, new_subscriber: PolygonEventConsumer):
        """
        The subscriber will be notified about future polygon events.
        :param new_subscriber: the new subscriber
        """
        self._subscribers.append(new_subscriber)

    def unsubscribe(self, subscriber: PolygonEventConsumer):
        """
        The subscriber will no longer be notified about future polygon events.
        :param subscriber: the subscriber
        """
        self._subscribers.remove(subscriber)

    def _distribute_polygon_added(self, event: PolygonAdded):
        for subscriber in self._subscribers:
            subscriber.process_added_polygon(event)

    def _distribute_polygon_deleted(self, event: PolygonDeleted):
        for subscriber in self._subscribers:
            subscriber.process_deleted_polygon(event)

    def _distribute_changed_polygon(self, event: PolygonChanged):
        for subscriber in self._subscribers:
            subscriber.process_changed_polygon(event)
