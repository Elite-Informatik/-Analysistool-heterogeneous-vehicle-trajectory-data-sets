from typing import List

from src.controller.output_handling.abstract_event import Event
from src.controller.output_handling.event import RefreshTrajectoryData
from src.view.event_handler.distributors.distributor import Distributor
from src.view.event_handler.event_consumers import TrajectoryEventConsumer


class TrajectoryEventDistributor(Distributor):
    """
    A distributor that notifies the trajectory event consumers about trajectory events.
    """

    def __init__(self):
        super().__init__()
        self._subscribers: List[TrajectoryEventConsumer] = []

    def distribute_event(self, event: Event):
        """
        distributes the event to the subscribers
        :param event: the event
        """
        if type(event) == RefreshTrajectoryData:
            self._distribute_refresh_trajectory_data(event)

    def subscribe(self, new_subscriber: TrajectoryEventConsumer):
        """
        The subscriber will be notified about future trajectory events.
        :param new_subscriber: the new subscriber
        """
        self._subscribers.append(new_subscriber)

    def unsubscribe(self, subscriber: TrajectoryEventConsumer):
        """
        The subscriber will no longer be notified about future trajectory events.
        :param subscriber: the subscriber
        """
        self._subscribers.remove(subscriber)

    def _distribute_refresh_trajectory_data(self, event: RefreshTrajectoryData):
        for subscriber in self._subscribers:
            subscriber.process_refreshed_trajectory_data(event)
