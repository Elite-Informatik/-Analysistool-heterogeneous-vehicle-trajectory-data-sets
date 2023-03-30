import tkinter as tk

from src.view.user_interface.static_windows.main_window.main_window_factory import MainWindowFactory
from src.view.user_interface.static_windows.ui_element import UiElement
from src.view.user_interface.static_windows.window import Window
from src.view.user_interface.ui_util.texts import EnglishTexts


class MainWindow(Window):
    """
    The Main Window of the application. It is the root of the MainWindowElement-Tree.
    It holds the Menubar and the MainWindowBaseFrame as its direct children
    """

    def __init__(self, factory: MainWindowFactory, close_application: callable):
        super().__init__()

        self._factory = factory
        self._base_frame: UiElement = factory.create_main_window_base_frame()
        self._menu_bar = factory.create_menu_bar()
        self._close_application_command = close_application

    def run(self):
        """
        See documentation of the abstract window class
        """
        self._window = tk.Tk()
        self._window.title(EnglishTexts.MAIN_WINDOW_TITLE.value)
        self._window.protocol("WM_DELETE_WINDOW", self.close_application)

        base_frame = self._base_frame.build(self._window)
        base_frame.grid(sticky="nsew")

        menu_visible = self._menu_bar.build(master=self._window)
        self._window.config(menu=menu_visible)
        # make sure that the window content expands
        self._window.columnconfigure(0, weight=1)
        self._window.rowconfigure(0, weight=1)

        self._window.mainloop()

    def destroy(self):
        """
        See documentation of the abstract window class
        """
        self._base_frame.destroy()
        self._menu_bar.destroy()
        self._window.destroy()

    def close_application(self):
        """
        gets called when the user closes the window
        """
        self._close_application_command()
        self.destroy()
