import tkinter as tk

from src.controller.event import SettingsChanged

from src.view.event_handler import EventHandler
from src.view.user_interface.static_windows.settings_window.settings_window import SettingsWindow
from src.view.user_interface.static_windows.settings_window.settings_window_factory import SettingsWindowFactory
from test.view.main_window.stumps import ControllerStump
from test.view.main_window.stumps import DataRequestStump

event_handler = EventHandler()
controller_communication = ControllerStump(event_handler=event_handler)
data_request = DataRequestStump()

if __name__ == "__main__":
    root = tk.Tk()
    dataset_window_factory = SettingsWindowFactory(event_handler=event_handler,
                                                   controller_communication=controller_communication,
                                                   data_request=data_request)
    dataset_window = SettingsWindow(factory=dataset_window_factory)
    event_handler.notify_event(SettingsChanged())

    dataset_window.run()

    root.withdraw()
    root.mainloop()
