import tkinter as tk
from abc import ABC
from abc import abstractmethod

from src.view.controller_communication.controller_communication import ControllerCommunication
from src.view.data_request.data_request import DataRequest
from src.view.event_handler.event_handler import IEventHandlerSubscribe


class UiElement(ABC):
    """
    A UiElement is a Wrapper for tkinter Frame that defines the design and functionality of
    a certain user interface element. It has access to the system interfaces via the event handler,
    controller communication and data request interfaces. A Ui Element is an Element of an ui element tree
    it will be created at program start and will be alive during the entire runtime of the application.
    The ui element can build a concreate element (a tkinter widget) that will be bound into a window and
    will be visible to the user. Via this element the user interacts with the ui Element class.
    """

    def __init__(self,
                 controller_communication: ControllerCommunication,
                 data_request: DataRequest,
                 event_handler: IEventHandlerSubscribe):
        self._controller_communication: ControllerCommunication = controller_communication
        self._data_request: DataRequest = data_request
        self._event_handler: IEventHandlerSubscribe = event_handler

        self._base_frame: tk.Widget = None

    @abstractmethod
    def build(self, master: tk.Widget) -> tk.Widget:
        """
        Builds the UiElement and returns a tkinter widget wich will be bound into a different UiElement or Window.
        With the tkinter widget the user can now interact with the UiElement class.
        """
        pass

    @abstractmethod
    def destroy(self):
        """
        Destroys the tkinter widget that belongs to the Element.
        Furthermore, the function resets the state of the Element to a safe state so the element can be build again
        """
        pass
