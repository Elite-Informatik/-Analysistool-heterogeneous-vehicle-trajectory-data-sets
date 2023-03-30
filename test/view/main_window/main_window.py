from src.controller.controller import Controller
from src.view.controller_communication.controller_communication import ControllerCommunication
from src.view.event_handler.event_handler import EventHandler
from src.view.user_interface.static_windows.main_window.main_window import MainWindow
from src.view.user_interface.static_windows.main_window.main_window_factory import MainWindowFactory

communication_facade = Controller().communication_facade

event_handler = EventHandler()
controller_communication = ControllerCommunication(controller_communication=communication_facade)
# data_request = DataRequest(DataRequestFacade())

if __name__ == "__main__":
    factory = MainWindowFactory(event_handler=event_handler, controller_communication=controller_communication,
                                data_request=None)

    main_window = MainWindow(factory)
    main_window.run()
