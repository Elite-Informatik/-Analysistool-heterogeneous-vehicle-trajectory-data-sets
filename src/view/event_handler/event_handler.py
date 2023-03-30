from src.controller.output_handling.abstract_event import Event
from src.controller.output_handling.event import *
from .distributors import AnalysisEventDistributor
from .distributors import DatasetEventDistributor
from .distributors import FilterEventDistributor
from .distributors import PolygonEventDistributor
from .distributors import SettingsEventDistributor
from .distributors import TrajectoryEventDistributor
from .event_consumers import AnalysisEventConsumer
from .event_consumers import DatasetEventConsumer
from .event_consumers import FilterEventConsumer
from .event_consumers import PolygonEventConsumer
from .event_consumers import SettingsEventConsumer
from .event_consumers import TrajectoryEventConsumer
from .i_event_handler_notify import IEventHandlerNotify
from .i_event_hanlder_subscribe import IEventHandlerSubscribe
from ...data_transfer.content.logger import logging


class EventHandler(IEventHandlerNotify, IEventHandlerSubscribe):
    """
    The EventHandler takes in events and distributes them to the events consumers which want to consume the events.
    The class implements two interfaces. One interface is public to the external components and can be used to notify
    events. The other is used by view internal components to subscribe events groups so they get notified about
    the events of that group.
    """

    def __init__(self):
        self._filter_event_distributor: FilterEventDistributor = FilterEventDistributor()
        self._settings_event_distributor: SettingsEventDistributor = SettingsEventDistributor()
        self._trajectory_event_distributor: TrajectoryEventDistributor = TrajectoryEventDistributor()
        self._analysis_event_distributor: AnalysisEventDistributor = AnalysisEventDistributor()
        self._polygon_event_distributor: PolygonEventDistributor = PolygonEventDistributor()
        self._dataset_event_distributor: DatasetEventDistributor = DatasetEventDistributor()

        self._event_to_distributor = {FilterAdded: self._filter_event_distributor,
                                      FilterGroupAdded: self._filter_event_distributor,
                                      FilterChanged: self._filter_event_distributor,
                                      FilterGroupChanged: self._filter_event_distributor,
                                      FilterComponentDeleted: self._filter_event_distributor,
                                      FilterMovedToGroup: self._filter_event_distributor,
                                      PolygonAdded: self._polygon_event_distributor,
                                      PolygonDeleted: self._polygon_event_distributor,
                                      PolygonChanged: self._polygon_event_distributor,
                                      AnalysisAdded: self._analysis_event_distributor,
                                      AnalysisDeleted: self._analysis_event_distributor,
                                      AnalysisRefreshed: self._analysis_event_distributor,
                                      AnalysisChanged: self._analysis_event_distributor,
                                      AnalysisImported: self._analysis_event_distributor,
                                      DatasetAdded: self._dataset_event_distributor,
                                      DatasetDeleted: self._dataset_event_distributor,
                                      DatasetOpened: self._dataset_event_distributor,
                                      DatasetExported: self._dataset_event_distributor,
                                      RefreshTrajectoryData: self._trajectory_event_distributor,
                                      SettingsChanged: self._settings_event_distributor}

    @logging
    def notify_event(self, event: Event):
        distributor = self._event_to_distributor[event.__class__]
        distributor.distribute_event(event)

    def subscribe_filter_events(self, subscriber: FilterEventConsumer):
        self._filter_event_distributor.subscribe(subscriber)

    def subscribe_analysis_events(self, subscriber: AnalysisEventConsumer):
        self._analysis_event_distributor.subscribe(subscriber)

    def subscribe_polygon_events(self, subscriber: PolygonEventConsumer):
        self._polygon_event_distributor.subscribe(subscriber)

    def subscribe_dataset_events(self, subscriber: DatasetEventConsumer):
        self._dataset_event_distributor.subscribe(subscriber)

    def subscribe_trajectory_events(self, subscriber: TrajectoryEventConsumer):
        self._trajectory_event_distributor.subscribe(subscriber)

    def subscribe_settings_events(self, subscriber: SettingsEventConsumer):
        self._settings_event_distributor.subscribe(subscriber)

    def unsubscribe_filter_events(self, subscriber: FilterEventConsumer):
        self._filter_event_distributor.unsubscribe(subscriber)

    def unsubscribe_analysis_events(self, subscriber: AnalysisEventConsumer):
        self._analysis_event_distributor.unsubscribe(subscriber)

    def unsubscribe_polygon_events(self, subscriber: PolygonEventConsumer):
        self._polygon_event_distributor.unsubscribe(subscriber)

    def unsubscribe_dataset_events(self, subscriber: DatasetEventConsumer):
        self._dataset_event_distributor.unsubscribe(subscriber)

    def unsubscribe_trajectory_events(self, subscriber: TrajectoryEventConsumer):
        self._trajectory_event_distributor.unsubscribe(subscriber)

    def unsubscribe_settings_events(self, subscriber: SettingsEventConsumer):
        self._settings_event_distributor.unsubscribe(subscriber)
