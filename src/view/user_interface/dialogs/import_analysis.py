import os.path
import tkinter as tk
from tkinter import ACTIVE
from tkinter import END
from tkinter import LEFT
from tkinter import filedialog
from tkinter.messagebox import showerror
from tkinter.simpledialog import Dialog

from src.view.user_interface.ui_util.texts import EnglishTexts


class ImportAnalysisDialog(Dialog):
    """
    Implements a dialog to create a new analysis
    """

    def __init__(self):
        """
        creates a new CreateAnalysisDialog.
        The dialog will be immediately displayed on the screen when the constructor is called.
        """
        self._path_entry = None
        self._selected_path: str = None
        self._valid_input = False
        super().__init__(parent=None, title=EnglishTexts.IMPORT_ANALYSIS_DIALOG_TITLE.value)

    def body(self, master):

        body_frame = tk.Frame(master=master)
        select_path_instruction = tk.Label(master=body_frame, text=EnglishTexts.ENTER_PATH.value, anchor="w")
        select_path_instruction.grid(row=0, column=0, sticky="w", pady=5, padx=5)
        self._path_entry = tk.Entry(master=body_frame)
        self._path_entry.grid(row=0, column=1, sticky="w")
        select_path_btn = tk.Button(master=body_frame, text=EnglishTexts.SELECT_PATH_BTN_NAME.value,
                                    command=self.__on_select_path)
        select_path_btn.grid(row=0, column=2)

        body_frame.pack(pady=50)

    def buttonbox(self):

        box = tk.Frame(self)

        w = tk.Button(box, text=EnglishTexts.OK_BTN_NAME.value, width=10, command=self.ok, default=ACTIVE)
        w.pack(side=LEFT, padx=5, pady=5)
        w = tk.Button(box, text=EnglishTexts.CANCEL_BTN_NAME.value, width=10, command=self.cancel)
        w.pack(side=LEFT, padx=5, pady=5)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

        box.pack(side="bottom")

    def __on_select_path(self):
        file_path: str = filedialog.askopenfilename()
        self._path_entry.insert(END, file_path)

    def ok(self):

        if self.validate(self._path_entry.get()):
            self._selected_path = self._path_entry.get()
            self.destroy()
        else:
            showerror(EnglishTexts.ERROR_INVALID_INPUT.value, EnglishTexts.INSTRUCTION_INVALID_INPUT.value)
            pass

    def cancel(self):

        self.destroy()

    def validate(self, selected: str) -> bool:

        self._valid_input = os.path.isfile(selected)
        return self._valid_input

    @property
    def selected_path(self) -> str:

        return self._selected_path

    @property
    def valid_input(self) -> bool:

        return self._valid_input
