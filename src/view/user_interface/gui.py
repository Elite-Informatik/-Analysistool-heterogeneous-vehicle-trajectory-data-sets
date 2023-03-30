from src.view.controller_communication.controller_communication import ControllerCommunication
from src.view.data_request.data_request import DataRequest
from src.view.event_handler import EventHandler
from src.view.user_interface.dialogs.manual.manual_window import ManualWindow
from src.view.user_interface.static_windows.dataset_window.dataset_window import DatasetWindow
from src.view.user_interface.static_windows.dataset_window.dataset_window_factory import DatasetWindowFactory
from src.view.user_interface.static_windows.main_window.main_window import MainWindow
from src.view.user_interface.static_windows.main_window.main_window_factory import MainWindowFactory
from src.view.user_interface.static_windows.settings_window.settings_window import SettingsWindow
from src.view.user_interface.static_windows.settings_window.settings_window_factory import SettingsWindowFactory
from src.view.user_interface.static_windows.start_window.start_window import StartWindow
from src.view.user_interface.static_windows.start_window.start_window_factory import StartWindowFactory


class GUI:
    """
    Class that manages the user interface on the Top Level.
    It holds the root of all UiElement Trees which are the windows.
    It is used to switch between the windows of the application.
    """
    START_WINDOW: StartWindow = None
    MAIN_WINDOW: MainWindow = None
    DATASET_WINDOW: DatasetWindow = None
    SETTINGS_WINDOW: SettingsWindow = None
    MANUAL_WINDOW: ManualWindow = None

    @staticmethod
    def initialize(data_request: DataRequest,
                   controller_communication: ControllerCommunication,
                   event_handler: EventHandler):
        """
        The initialize function creates the factories for the UiElement Trees and
        the root af the tress. It passes the factories to the corresponding root.
        The root cant that create further Elements. After this function is called
        all UiElements are initialized and ready to receive and process events.
        Event though the concrete Windows arent displayed on the screen yet.
        """
        start_window_factory = StartWindowFactory(event_handler=event_handler,
                                                  controller_communication=controller_communication,
                                                  data_request=data_request)
        main_window_factory = MainWindowFactory(event_handler=event_handler,
                                                controller_communication=controller_communication,
                                                data_request=data_request)
        dataset_window_factory = DatasetWindowFactory(event_handler=event_handler,
                                                      controller_communication=controller_communication,
                                                      data_request=data_request)
        settings_window_factory = SettingsWindowFactory(event_handler=event_handler,
                                                        controller_communication=controller_communication,
                                                        data_request=data_request)

        GUI.START_WINDOW = StartWindow(factory=start_window_factory,
                                       close_application=controller_communication.close_application)
        GUI.MAIN_WINDOW = MainWindow(factory=main_window_factory,
                                     close_application=controller_communication.close_application)
        GUI.DATASET_WINDOW = DatasetWindow(factory=dataset_window_factory)
        GUI.SETTINGS_WINDOW = SettingsWindow(factory=settings_window_factory)
        GUI.MANUAL_WINDOW = ManualWindow()

    @staticmethod
    def gui_start_up():
        """
        Creates the first window that will be visible to the user
        """
        GUI.START_WINDOW.run()

    @staticmethod
    def gui_stop():
        """
        Destroys all windows. And closes the entire User interface.
        The tkinter-event loop of all running windows will be stopped
        and the application will eventually stop.
        """
        GUI.SETTINGS_WINDOW.destroy()
        GUI.DATASET_WINDOW.destroy()
        GUI.START_WINDOW.destroy()
        GUI.MAIN_WINDOW.destroy()

    @staticmethod
    def open_dataset_window():
        """
        The dataset will be opened and displayed on the screen.
        """
        GUI.DATASET_WINDOW.run()

    @staticmethod
    def open_settings_window():
        """
        The settings window will be opened and displayed on the screen.
        """
        GUI.SETTINGS_WINDOW.run()

    @staticmethod
    def open_manual_window():
        """
        The manual window will be opened and displayed on the screen.
        """
        GUI.MANUAL_WINDOW.run()

    @staticmethod
    def close_settings_window():
        """
        The settings window will be closed and not displayed on the screen anymore
        """
        GUI.SETTINGS_WINDOW.destroy()

    @staticmethod
    def switch_to_main_window():
        """
        The start window will be closed and the main window will be
        displayed on the screen instead.
        """
        GUI.START_WINDOW.destroy()
        GUI.MAIN_WINDOW.run()
