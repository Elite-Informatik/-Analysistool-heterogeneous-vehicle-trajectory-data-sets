from src.controller.controller import IController
from src.view.controller_communication.controller_communication import ControllerCommunication
from src.view.data_request.data_request import DataRequest
from src.view.event_handler import EventHandler
from src.view.event_handler import IEventHandlerNotify
from src.view.iview import IView
from src.view.iview_application import IViewApplication
from src.view.user_input_request.user_input_request import UserInputRequestFacade
from src.view.user_interface.gui import GUI


class View(IView, IViewApplication):
    """
    The View class is used to set up and initialize the View.
    It has no user interface related functionalities and is only used
    by other components to handle the View in a compact form.
    To set up the View you have to create a View instance and
    set the controller. Then the View is fully initialized.
    The concrete User Interface can than be started and stopped.
    """

    def __init__(self):
        """
        initializes the provided interface of the View. The variables that are used to access the
        required interface are declared but not initialized because they require the controller.
        """
        # initialize events handler
        self._event_handler = EventHandler()
        self._user_input_request = UserInputRequestFacade()

        # declare required interfaces
        self._controller_communication = None
        self._data_request = None

    def set_controller(self, controller: IController):
        """
        sets the required interfaces that the view needs to access the controller.
        The GUI is initialized. All UiElements can receive and process events from here on.
        """
        self._controller_communication = ControllerCommunication(controller.communication_facade)
        self._data_request = DataRequest(controller.data_request_facade)
        GUI.initialize(data_request=self._data_request,
                       controller_communication=self._controller_communication,
                       event_handler=self._event_handler)

    def start(self):
        """
        Starts the gui and makes the first Window visible to the user.
        The user can now interact with the application vie the user interface.
        """
        GUI.gui_start_up()

    def stop(self):
        """
        Closes all Windows. The user cant interact with the application anymore.
        """
        GUI.gui_stop()

    def event_handler(self) -> IEventHandlerNotify:
        return self._event_handler

    def user_input_request(self) -> UserInputRequestFacade:
        return self._user_input_request
