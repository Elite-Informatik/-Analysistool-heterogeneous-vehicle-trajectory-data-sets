from typing import List

from src.controller.output_handling.abstract_event import Event
from src.controller.output_handling.event import AnalysisAdded, AnalysisImported
from src.controller.output_handling.event import AnalysisChanged
from src.controller.output_handling.event import AnalysisDeleted
from src.controller.output_handling.event import AnalysisRefreshed
from src.view.event_handler.distributors.distributor import Distributor
from src.view.event_handler.event_consumers import AnalysisEventConsumer


class AnalysisEventDistributor(Distributor):
    """
    The AnalysisEventDistributor notifies its subscribers about all analysis events.
    """

    def __init__(self):
        super().__init__()
        self._subscribers: List[AnalysisEventConsumer] = []

    def distribute_event(self, event: Event):
        """
        selects the interface method that should be called on the subscribers, based on the event type
        :param event: the event
        """
        if type(event) == AnalysisAdded:
            self._distribute_added_analysis(event)
        if type(event) == AnalysisDeleted:
            self._distribute_deleted_analysis(event)
        if type(event) == AnalysisRefreshed:
            self._distribute_refreshed_analysis(event)
        if type(event) == AnalysisChanged:
            self._distribute_changed_analysis(event)
        if type(event) == AnalysisImported:
            self._distribute_imported_analysis(event)

    def subscribe(self, new_subscriber: AnalysisEventConsumer):
        """
        subscriber will be notified about future analysis events.
        :param new_subscriber: object that implements the AnalysisEventConsumer interface
        """
        self._subscribers.append(new_subscriber)

    def unsubscribe(self, subscriber: AnalysisEventConsumer):
        """
        the subscriber will no longer be notified about future analysis events.
        If the given object is not a subscriber nothing happens.
        :param subscriber: the potential subscriber
        """
        self._subscribers.remove(subscriber)

    def _distribute_added_analysis(self, event: AnalysisAdded):
        """
        calls the method that processes an AnalysisAdded event on all subscribers and passes the event to them.
        :param event: the event containing the id of the analysis
        """
        for subscriber in self._subscribers:
            subscriber.process_added_analysis(event)

    def _distribute_imported_analysis(self, event: AnalysisImported):
        for subscriber in self._subscribers:
            subscriber.process_imported_analysis(event)

    def _distribute_deleted_analysis(self, event: AnalysisDeleted):
        """
        calls the method that processes an AnalysisDeleted event on all subscribers and passes the event to them.
        :param event: the event containing the id of the deleted analysis
        """
        for subscriber in self._subscribers:
            subscriber.process_deleted_analysis(event)

    def _distribute_refreshed_analysis(self, event: AnalysisRefreshed):
        """
        calls the method that processes an AnalysisRefreshed event on all subscribers and passes the event to them.
        :param event: the event containing the id of the refreshed analysis
        """
        for subscriber in self._subscribers:
            subscriber.process_refreshed_analysis(event)

    def _distribute_changed_analysis(self, event: AnalysisChanged):
        """
        calls the method that processes an AnalysisChanged event on all subscribers and passes the event to them.
        :param event: the event containing the id of the changed analysis
        """
        for subscriber in self._subscribers:
            subscriber.process_changed_analysis(event)
