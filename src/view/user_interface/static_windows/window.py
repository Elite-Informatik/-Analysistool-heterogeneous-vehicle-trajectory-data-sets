import tkinter as tk
from abc import ABC
from abc import abstractmethod


class Window(ABC):
    """
    abstract base class for all windows. It is a wrapper
    for the Tk class from the tkinter module.
    The Instances of the concrete Window classes should be
    alive on the whole runtime of the application. The concrete
    instances can than be used to create or destroy the actual window that
    is visible to the user. The concrete Windows are the root of all UiElement trees.
    """

    def __init__(self):
        self._window: tk.Tk = None

    @abstractmethod
    def run(self):
        """
        Builds and starts the window. The window will be displayed on the screen and the
        user can interact with the window now.
        """
        pass

    @abstractmethod
    def destroy(self):
        """
        If a window that is visible to the user exists. The window will be destroyed
        and wont be visible to the user anymore. The Window Instance it self should bot be deleted
        """
        pass
