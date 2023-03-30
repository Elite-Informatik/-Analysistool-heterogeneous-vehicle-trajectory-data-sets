import os
import tkinter as tk
from tkinter import ACTIVE
from tkinter import END
from tkinter import LEFT
from tkinter import filedialog
from tkinter.messagebox import showerror
from tkinter.simpledialog import Dialog
from typing import Optional

from src.view.user_interface.ui_util.texts import EnglishTexts


class ExportDatasetDialog(Dialog):
    """
    represents a dialog to export a dataset.
    The dialog will be immediately displayed on the screen when the constructor is called.
    """

    def __init__(self):
        """
        creates a new ExportDatasetDialog
        """
        self._path_entry = None
        self._file_name_entry = None
        self._selected_path: Optional[str] = None
        self._valid_input = False
        super().__init__(parent=None, title=EnglishTexts.EXPORT_DATASET_DIALOG_NAME.value)

    def body(self, master):

        body_frame = tk.Frame(master=master)

        path_label = tk.Label(master=body_frame, text=EnglishTexts.INSTRUCTION_ENTER_DIRECTORY.value, anchor="w")
        path_label.grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self._path_entry = tk.Entry(master=body_frame)
        self._path_entry.grid(row=0, column=1, sticky="w")
        select_path_btn = tk.Button(master=body_frame, text=EnglishTexts.SELECT_DIRECTORY_BTN_NAME.value,
                                    command=self.__on_select_path)
        select_path_btn.grid(row=0, column=2)

        body_frame.pack(pady=50)

    def __on_select_path(self):
        folder_path = filedialog.askdirectory()
        self._path_entry.insert(END, folder_path)

    def buttonbox(self):
        box = tk.Frame(self)

        w = tk.Button(box, text=EnglishTexts.OK_BTN_NAME.value, width=10, command=self.ok, default=ACTIVE)
        w.pack(side=LEFT, padx=5, pady=5)
        w = tk.Button(box, text=EnglishTexts.CANCEL_BTN_NAME.value, width=10, command=self.cancel)
        w.pack(side=LEFT, padx=5, pady=5)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

        box.pack(side="bottom")

    def ok(self):
        if self.validate():
            self._selected_path = self._path_entry.get()
            self.destroy()

    def cancel(self):
        self.destroy()

    def validate(self) -> bool:
        path = self._path_entry.get()
        if not os.path.exists(path):
            showerror(message=EnglishTexts.INVALID_FILE_PATH.value.format(path))
            self._valid_input = False
            return False
        self._valid_input = True
        return True

    @property
    def selected_path(self) -> str:
        return self._selected_path

    @property
    def valid_input(self) -> bool:
        return self._valid_input
