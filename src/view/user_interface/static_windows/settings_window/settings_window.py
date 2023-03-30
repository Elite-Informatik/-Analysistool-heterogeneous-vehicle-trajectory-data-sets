import tkinter as tk

from src.view.user_interface.static_windows.settings_window.settings_window_factory import SettingsWindowFactory
from src.view.user_interface.static_windows.window import Window
from src.view.user_interface.ui_util.texts import EnglishTexts


class SettingsWindow(Window):
    """
    """

    def __init__(self, factory: SettingsWindowFactory):
        super().__init__()

        self._factory = factory
        self._base_frame = factory.create_base_frame()

    def run(self):
        """
        See documentation of the abstract window class
        """
        self._window = tk.Toplevel()
        self._window.columnconfigure(0, weight=1)
        self._window.rowconfigure(1, weight=1)
        self._window.resizable(width=False, height=False)
        self._window.grab_set()
        self._window.title(EnglishTexts.SETTINGS_WINDOW_TITLE.value)
        self._window.rowconfigure(0, weight=1)
        self._window.columnconfigure(0, weight=1)
        self._window.protocol("WM_DELETE_WINDOW", self.destroy)

        settings_frame = self._base_frame.build(self._window)
        settings_frame.grid(column=0, row=0, sticky="nsew")

        self._window.mainloop()

    def destroy(self):
        """
        See documentation of the abstract window class
        """
        self._base_frame.destroy()
        self._window.destroy()
