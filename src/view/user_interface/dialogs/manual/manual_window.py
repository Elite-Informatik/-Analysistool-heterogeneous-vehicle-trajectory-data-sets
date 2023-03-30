import tkinter as tk

from src.view.user_interface.dialogs.manual.manual_baseframe import ManualBaseFrame
from src.view.user_interface.static_windows.window import Window
from src.view.user_interface.ui_util.texts import EnglishTexts


class ManualWindow(Window):
    """
    This dialog is used to display the settings. It is no subclass of Dialog since you can't choose/ cancel anything.
    """

    def __init__(self):
        super().__init__()
        self._base_frame = ManualBaseFrame()

    def run(self):
        """
        Window is a TopLevel Window. It as a main Tk instance required to run the
        dataset window. In the current implementation the Tk instance will be the Main-Window
        of the application
        """
        self._window = tk.Toplevel()
        self._window.grab_set()
        self._window.title(EnglishTexts.MANUAL_WINDOW_TITLE.value)
        self._window.columnconfigure(0, weight=1)
        self._window.rowconfigure(0, weight=1)

        manual_frame = self._base_frame.build(self._window)
        manual_frame.grid(column=0, row=0, sticky="nsew")

    def destroy(self):
        """
        self._window has to be set to None so it is clearly indicated that
        the window is not build currently
        """
        self._base_frame.destroy()
        self._window.grab_release()
        if self._window is not None:
            self._window.destroy()
        self._window = None
