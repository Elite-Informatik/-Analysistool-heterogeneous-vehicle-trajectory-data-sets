
import tkinter as tk

from src.view.user_interface.dialogs.manual.manual_notebook import ManualNotebook


class ManualBaseFrame:
    """
    UiElement that is used to display the manual.
    """

    def __init__(self):
        self._base_frame: tk.Frame = None
        self._notebook: ManualNotebook = None

    def build(self, master: tk.Widget) -> tk.Widget:
        """
        builds the manual baseframe
        :param master: the master of the baseframe
        :return:       the new manual base frame
        """
        self._base_frame = tk.Frame(master=master)
        self._base_frame.columnconfigure(0, weight=1)
        self._base_frame.rowconfigure(0, weight=1)

        self._notebook = ManualNotebook().build(self._base_frame)
        self._notebook.pack(fill="both", expand=True)

        return self._base_frame

    def destroy(self):
        """
        destroys the base frame.
        """
        self._base_frame.destroy()
