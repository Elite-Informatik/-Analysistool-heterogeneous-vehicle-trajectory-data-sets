import tkinter as tk

from src.controller.event import DatasetAdded

from src.view.event_handler import EventHandler
from src.view.user_interface.static_windows.dataset_window.dataset_window import DatasetWindow
from src.view.user_interface.static_windows.dataset_window.dataset_window_factory import DatasetWindowFactory
from test.view.main_window.stumps import ControllerStump
from test.view.main_window.stumps import DataRequestStump

event_handler = EventHandler()
controller_communication = ControllerStump(event_handler=event_handler)
data_request = DataRequestStump()

if __name__ == "__main__":

    root = tk.Tk()
    dataset_window_factory = DatasetWindowFactory(event_handler=event_handler,
                                                  controller_communication=controller_communication,
                                                  data_request=data_request)
    dataset_window = DatasetWindow(factory=dataset_window_factory)
    datasets = data_request.get_dataset_ids()
    for dataset in datasets:
        event_handler.notify_event(DatasetAdded(_id=dataset))

    dataset_window.run()

    root.withdraw()
    root.mainloop()
