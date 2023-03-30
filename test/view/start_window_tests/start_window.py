from unittest.mock import MagicMock
from uuid import uuid4

from src.data_transfer import DatasetRecord
from src.view.controller_communication.controller_communication import ControllerCommunication
from src.view.data_request.data_request import DataRequest
from src.view.event_handler.event_handler import EventHandler
from src.view.user_interface.static_windows.start_window.start_window import StartWindow
from src.view.user_interface.static_windows.start_window.start_window_factory import StartWindowFactory

event_handler = EventHandler()

example_datasets = [DatasetRecord(_id=uuid4(), _name="Datensatz1", _size=1000),
                    DatasetRecord(_id=uuid4(), _name="Datensat2", _size=1000),
                    DatasetRecord(_id=uuid4(), _name="Datensa3", _size=1000),
                    DatasetRecord(_id=uuid4(), _name="Datens4", _size=1000),
                    DatasetRecord(_id=uuid4(), _name="Daten5", _size=1000)]

data_request = DataRequest(data_request=None)

controller_communication = ControllerCommunication(controller_communication=None)
controller_communication.import_dataset = MagicMock(return_value=None)
controller_communication.open_dataset = MagicMock(return_value=None)

if __name__ == "__main__":
    factory = StartWindowFactory(event_handler=event_handler, data_request=data_request,
                                 controller_communication=controller_communication)
    start_window = StartWindow(factory=factory)
    start_window.run()
