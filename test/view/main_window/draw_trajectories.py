from src.controller.output_handling.event import RefreshTrajectoryData
from src.view.event_handler import EventHandler
from src.view.user_interface.gui import GUI
from test.view.main_window.stumps import ControllerStump
from test.view.main_window.stumps import DataRequestStump

event_handler = EventHandler()

controller = ControllerStump(event_handler=event_handler)
data_request = DataRequestStump()

if __name__ == "__main__":
    GUI.initialize(event_handler=event_handler, data_request=data_request, controller_communication=controller)
    event_handler.notify_event(RefreshTrajectoryData())
    GUI.MAIN_WINDOW.run()
