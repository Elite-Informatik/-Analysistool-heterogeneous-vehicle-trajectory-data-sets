import tkinter as tk

from src.view.user_interface.static_windows.start_window.start_window_factory import StartWindowFactory
from src.view.user_interface.static_windows.window import Window
from src.view.user_interface.ui_util.texts import EnglishTexts


class StartWindow(Window):
    """
    Implements the start window of the application.
    The StartWindow is the root of the Element Tree for the start window.
    """

    def __init__(self, factory: StartWindowFactory, close_application: callable):
        """
        Creates a new StartWindow instance and all UiElements that belong to the start window.
        """
        super().__init__()
        self._factory = factory
        self._base_frame = factory.create_start_window_base_frame()

        self._close_application_command = close_application

    def run(self):
        """
        See documentation of the abstract window class
        """
        self._window = tk.Tk()
        self._window.geometry("800x400")
        self._window.title(EnglishTexts.START_WINDOW_TITLE.value)
        self._window.protocol("WM_DELETE_WINDOW", self.close_application)

        frame = self._base_frame.build(master=self._window)
        frame.pack()
        self._window.mainloop()

    def destroy(self):
        """
        See documentation of the abstract window class
        """
        self._base_frame.destroy()
        self._window.destroy()
        self._window = None

    def close_application(self):
        """
        Closes the application. The Start Window is the main window of the application at the application start.
        Thus if the start window gets closed the application closes.
        """
        self._close_application_command()
        self.destroy()
