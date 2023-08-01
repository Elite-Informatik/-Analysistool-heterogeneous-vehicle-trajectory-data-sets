from abc import ABC
from typing import List
from typing import Optional

from src.controller.output_handling.abstract_event import Event
from src.controller.output_handling.event_manager import IEventManager
from src.controller.output_handling.irequest_manager import IRequestManager
from src.data_transfer.record import ErrorRecord
from src.model.i_error_handler import IErrorHandler


class AbstractManager(ABC):

    def __init__(self):
        """
        Constructor for an abstract manager. The error origins are expected to be set from the subclass via direct
        appending to the list. The events represent an event queue.
        """
        self._event_manager: Optional[IEventManager] = None
        self.request_manager: Optional[IRequestManager] = None
        self.events: List[Event] = list()

    def handle_event(self):
        events = self.events.copy()
        self.events.clear()
        self._event_manager.send_events(events=events)

    def handle_error(self, error_origins: List[IErrorHandler], meta_info: str = ""):
        """
        The default way of handling an error. The errors are queried from the possible origins. The meta-info
        provides additional information from the concrete respective manager. The errors are directly sent to the
        request_manager without further checking.
        If a more detailed error analysis is expected, the request_manager can be used in the concrete submanagers.
        For example, when dealing with a user request selection.

        :param error_origins: The possible origins of the error
        :param meta_info: Additional information of the manager (i.e. where the error happened in the manager's
        execution)
        """
        for origin in error_origins:
            errors = origin.get_errors()
            if not errors:
                continue

            # Add additional information from the manager and append it to the error records
            meta_errors: List[ErrorRecord] = []
            for error in errors:
                meta_errors.append(ErrorRecord(error_type=error.error_type, args=error.args + meta_info))
            self.request_manager.send_errors(meta_errors)

    def set_event_manager(self, event_manager: IEventManager):
        """
        Sets the event manager for the manager. This is necessary for the manager to be able to send events.
        :param event_manager: The event manager to set.
        """
        self._event_manager = event_manager

    def set_request_manager(self, request_manager: IRequestManager):
        """
        Sets the request manager for the manager. This is necessary for the manager to be able to send requests.
        :param request_manager: The request manager to set.
        """
        self.request_manager = request_manager
