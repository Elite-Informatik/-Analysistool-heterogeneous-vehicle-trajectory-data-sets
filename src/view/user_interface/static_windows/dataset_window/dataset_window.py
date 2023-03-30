import tkinter as tk

from src.view.user_interface.static_windows.dataset_window.dataset_window_factory import DatasetWindowFactory
from src.view.user_interface.static_windows.ui_element import UiElement
from src.view.user_interface.static_windows.window import Window
from src.view.user_interface.ui_util.texts import EnglishTexts


class DatasetWindow(Window):
    """
    Class that defines and handles the dataset window.
    Root of the Dataset UiElement-Tree.
    """

    def __init__(self, factory: DatasetWindowFactory):
        """
        Creates a new Dataset Window instance.
        :param factory: A factory that is used to create the UiElements of the dataset window.
        """
        super().__init__()

        self._factory = factory
        self._base_frame: UiElement = self._factory.create_dataset_base_frame()

    def run(self):
        """
        Window is a TopLevel Window. It as a main Tk instance required to run the
        dataset window. In the current implementation the Tk instance will be the Main-Window
        of the application
        """
        self._window = tk.Toplevel()
        self._window.grab_set()
        self._window.title(EnglishTexts.DATASET_WINDOW_TITLE.value)
        self._window.columnconfigure(0, weight=1)
        self._window.rowconfigure(0, weight=1)

        dataset_frame = self._base_frame.build(self._window)
        dataset_frame.grid(column=0, row=0, sticky="nsew")

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
