from typing import List

from src.controller.output_handling.abstract_event import Event
from src.controller.output_handling.event import FilterAdded
from src.controller.output_handling.event import FilterChanged
from src.controller.output_handling.event import FilterComponentDeleted
from src.controller.output_handling.event import FilterGroupAdded
from src.controller.output_handling.event import FilterGroupChanged
from src.controller.output_handling.event import FilterMovedToGroup
from src.view.event_handler.distributors.distributor import Distributor
from src.view.event_handler.event_consumers import FilterEventConsumer


class FilterEventDistributor(Distributor):
    """
    The distributor that notifies the the filter event consumers about filter related events
    """

    def __init__(self):
        super().__init__()
        self._subscribers: List[FilterEventConsumer] = []

    def distribute_event(self, event: Event):

        if type(event) == FilterComponentDeleted:
            self._distribute_filter_component_deleted(event)
        elif type(event) == FilterChanged:
            self._distribute_filter_changed(event)
        elif type(event) == FilterAdded:
            self._distribute_filter_added(event)
        elif type(event) == FilterGroupAdded:
            self._distribute_filter_group_added(event)
        elif type(event) == FilterGroupChanged:
            self._distribute_filter_group_changed(event)
        elif type(event) == FilterMovedToGroup:
            self._distribute_move_filter(event)

    def subscribe(self, new_subscriber: FilterEventConsumer):
        """
        The subscriber will be notified about future filter events.
        :param new_subscriber: the new subscriber
        """
        self._subscribers.append(new_subscriber)

    def unsubscribe(self, subscriber: FilterEventConsumer):
        """
        The subscriber will no longer be notified about future filter events.
        :param subscriber: the subscriber
        """
        self._subscribers.remove(subscriber)

    def _distribute_filter_component_deleted(self, event: FilterComponentDeleted):
        for subscriber in self._subscribers:
            subscriber.process_deleted_filter(event)

    def _distribute_filter_changed(self, event: FilterChanged):
        for subscriber in self._subscribers:
            subscriber.process_changed_filter(event)

    def _distribute_filter_added(self, event: FilterAdded):
        for subscriber in self._subscribers:
            subscriber.process_added_filter(event)

    def _distribute_filter_group_added(self, event: FilterGroupAdded):
        for subscriber in self._subscribers:
            subscriber.process_added_filter_group(event)

    def _distribute_filter_group_changed(self, event: FilterGroupChanged):
        for subscriber in self._subscribers:
            subscriber.process_changed_filter_group(event)

    def _distribute_move_filter(self, event: FilterMovedToGroup):
        for subscriber in self._subscribers:
            subscriber.process_moved_filter(event)
