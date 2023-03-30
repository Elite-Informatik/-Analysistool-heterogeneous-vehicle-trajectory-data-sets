from uuid import uuid4

from src.controller.output_handling.event import PolygonAdded
from src.view.event_handler.event_handler import EventHandler
from src.view.user_interface.static_windows.main_window.main_window import MainWindow
from src.view.user_interface.static_windows.main_window.main_window_factory import MainWindowFactory
from test.view.main_window.stumps import ControllerStump
from test.view.main_window.stumps import DataRequestStump

polygon1_uuid = uuid4()

event_handler = EventHandler()
data_request = DataRequestStump()

controller_communication = ControllerStump(event_handler)

if __name__ == "__main__":
    factory = MainWindowFactory(event_handler=event_handler, data_request=data_request,
                                controller_communication=controller_communication)

    main_window = MainWindow(factory=factory)

    event = PolygonAdded(_id=polygon1_uuid)
    event_handler.notify_event(event)

    main_window.run()
