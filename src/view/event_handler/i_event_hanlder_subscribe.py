from abc import ABC
from abc import abstractmethod

from src.view.event_handler.event_consumers import *


class IEventHandlerSubscribe(ABC):
    """
    This interface defines methods that are used by components in the system that want to be notified about events.
    The interface defines methods to subscribe and unsubscribe certain events groups. You can imagen this interface like
    the back of the events handler which is only seen by the view internal components. List of event groups:
    """

    @abstractmethod
    def subscribe_filter_events(self, subscriber: FilterEventConsumer):
        """
        Subscribes an object to the filter events. Thereby the object will be notified if a filter event occurs.
        :param subscriber: object that implements the FilterEventConsumer interface
        """
        pass

    @abstractmethod
    def subscribe_analysis_events(self, subscriber: AnalysisEventConsumer):
        """
        Subscribes an object to the analysis events. Thereby the object will be notified if an analysis event occurs.
        :param subscriber: object that implements the AnalysisEventConsumer interface
        """
        pass

    @abstractmethod
    def subscribe_polygon_events(self, subscriber: PolygonEventConsumer):
        """
        Subscribes an object to the polygon events. Thereby the object will be notified if a polygon event occurs.
        :param subscriber: object that implements the PolygonEventConsumer interface
        """
        pass

    @abstractmethod
    def subscribe_dataset_events(self, subscriber: DatasetEventConsumer):
        """
        Subscribes an object to the dataset events. Thereby the object will be notified if a dataset event occurs.
        :param subscriber: object that implements the DatasetEventConsumer interface
        """
        pass

    @abstractmethod
    def subscribe_trajectory_events(self, subscriber: TrajectoryEventConsumer):
        """
        Subscribes an object to the trajectory events. Thereby the object will be notified if a trajectory event occurs.
        :param subscriber: object that implements the TrajectoryEventConsumer interface
        """
        pass

    @abstractmethod
    def subscribe_settings_events(self, subscriber: SettingsEventConsumer):
        """
        Subscribes an object to the settings events. Thereby the object will be notified if a settings event occurs.
        :param subscriber: object that implements the SettingsEventConsumer interface
        """
        pass

    @abstractmethod
    def unsubscribe_filter_events(self, subscriber: FilterEventConsumer):
        """
        Unsubscribes an object from the filter events. If a filter event occurs the object will no longer be notified.
        If the Object was not subscribed, nothing happens.
        :param subscriber: potential event subscriber
        """
        pass

    @abstractmethod
    def unsubscribe_analysis_events(self, subscriber: AnalysisEventConsumer):
        """
        Unsubscribes an object from the analysis events. If an analysis event occurs
        the object will no longer be notified. If the Object was not subscribed, nothing happens.
        :param subscriber: potential event subscriber
        """
        pass

    @abstractmethod
    def unsubscribe_polygon_events(self, subscriber: PolygonEventConsumer):
        """
        Unsubscribes an object from the polygon events. If a polygon event occurs the object will no longer be notified.
        If the Object was not subscribed, nothing happens.
        :param subscriber: potential event subscriber
        """
        pass

    @abstractmethod
    def unsubscribe_dataset_events(self, subscriber: DatasetEventConsumer):
        """
        Unsubscribes an object from the dataset events. If a dataset event occurs the object will no longer be notified.
        If the Object was not subscribed, nothing happens.
        :param subscriber: potential event subscriber
        """
        pass

    @abstractmethod
    def unsubscribe_trajectory_events(self, subscriber: TrajectoryEventConsumer):
        """
        Unsubscribes an object from the trajectory events. If a trajectory event occurs
         the object will no longer be notified. If the Object was not subscribed, nothing happens.
        :param subscriber: potential event subscriber
        """
        pass

    @abstractmethod
    def unsubscribe_settings_events(self, subscriber: SettingsEventConsumer):
        """
        Unsubscribes an object from the settings events. If a settings event occurs
        the object will no longer be notified. If the Object was not subscribed, nothing happens.
        :param subscriber: potential event subscriber
        """
        pass
