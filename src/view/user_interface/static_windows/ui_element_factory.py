from abc import ABC

from src.view.controller_communication.controller_communication import ControllerCommunication
from src.view.data_request.data_request import DataRequest
from src.view.event_handler import IEventHandlerSubscribe


class UiElementFactory(ABC):
    """
    Each window has its own UiElementFactory that is used to create
    new UiElements of that window. The factory provides the ui elements
    with the unique instances of the event handler, controller communication and
    data request interfaces. Thereby the UiElements gain access to our internal system.
    The factory holds all system interfaces and decides which UiElement
    should have access to which system interfaces.
    """

    def __init__(self,
                 event_handler: IEventHandlerSubscribe,
                 controller_communication: ControllerCommunication,
                 data_request: DataRequest):
        """
        creates a new UiElementFactory and provides the factory with the system interfaces.
        """
        self._event_handler: IEventHandlerSubscribe = event_handler
        self._controller_communication: ControllerCommunication = controller_communication
        self._data_request: DataRequest = data_request
