import os.path
import tkinter as tk
from tkinter import filedialog
from tkinter.messagebox import showerror
from tkinter.simpledialog import Dialog
from typing import List

from src.data_transfer.content.data_types import DataTypes
from src.view.user_interface.ui_util.texts import EnglishTexts


class ImportDatasetDialog(Dialog):
    """
    Defines a Dialog in which the user can define path, _name and dataformat of a new dataset that the
    user wants to import.
    The dialog will be immediately displayed on the screen when the constructor is called.
    """

    def __init__(self, data_formats: List[str]):
        self._name_label = None
        self._name_entry = None
        self._format_label = None
        self._format_selector = None
        self._format_selector_view = None
        self._valid_input = False
        self._name = ""
        self._paths = []
        self._format = ""

        self._path_selectors: List[tk.StringVar] = []
        self._path_entry_fields: List[tk.Entry] = []

        self._formats_selectable = data_formats
        self._path_selection_frame: tk.Frame = None

        super().__init__(parent=None, title=EnglishTexts.IMPORT_DATASET_DIALOG_NAME.value)

    def body(self, master):
        """
        Defines how the body of the dialog looks like
        """
        self._name_label = tk.Label(master=master, text=EnglishTexts.CHOOSE_NAME_DATASET.value, anchor="w", width=15)
        self._name_label.grid(column=0, row=0, sticky="nsew")
        self._name_entry = tk.Entry(master=master, width=20)
        self._name_entry.grid(column=1, row=0, sticky="nsew")

        # self._format_label = tk.Label(master=master, text="format", anchor="w")
        # self._format_label.grid(column=0, row=1, sticky="nsew")
        self._format_selector = tk.StringVar()
        # arguments for the lambda are passed by tkinter but not used. If they are removed an exception is thrown
        self._format_selector.trace_add("write", callback=lambda a, b, c: self.build_path_options(master))
        # self._format_selector.set(value=self._formats_selectable[0])
        self._format_selector.set("format")
        self._format_selector_view = tk.OptionMenu(master, self._format_selector, *self._formats_selectable)
        self._format_selector_view.grid(column=2, row=0, sticky="nsew")

    def build_path_options(self, master):

        # reset path selectors and path selector frame to build it again clean
        if self._path_selection_frame is not None:
            self._path_selection_frame.destroy()
        self._path_selection_frame = tk.Frame(master=master)
        self._path_selectors = []
        self._path_entry_fields = []

        # build path selection entries depending on the selected file format
        file_format = self._format_selector.get()
        if file_format == DataTypes.HIGH_D.value:
            self.add_path_selection(master=self._path_selection_frame, row=1, label_name="recording:")
            self.add_path_selection(master=self._path_selection_frame, row=2, label_name="track_meta:")
            self.add_path_selection(master=self._path_selection_frame, row=3, label_name="tracks:")
        elif file_format == DataTypes.SIMRA.value:
            self.add_path_selection(master=self._path_selection_frame, row=1, label_name="directory:", directory=True)
        else:
            self.add_path_selection(master=self._path_selection_frame, row=0)

        self._path_selection_frame.grid(column=0, columnspan=3, row=2, sticky="nsew")

    def add_path_selection(self, master, row, label_name="path", directory=False):
        path_label = tk.Label(master=master, text=label_name, anchor="w", width=15)
        path_label.grid(row=row, column=0, sticky="nsew")
        path_selector = tk.StringVar()
        self._path_selectors.append(path_selector)
        path_entry = tk.Entry(master=master, textvariable=path_selector, width=20)
        path_entry.grid(column=1, row=row, sticky="nsew")
        if directory:
            path_select_button = tk.Button(master=master, text="Select",
                                           command=lambda: self.select_path_directory(string_var=path_selector))
        else:
            path_select_button = tk.Button(master=master, text="Select",
                                           command=lambda: self.select_path(string_var=path_selector))
        path_select_button.grid(column=2, row=row, sticky="nsew")

    def select_path(self, string_var):
        string_var.set(filedialog.askopenfilename())

    def select_path_directory(self, string_var):
        string_var.set(filedialog.askdirectory())

    def apply(self):
        """
        sets the _name, path and dataformat of the dialog based on the current user input.
        This method gets only called when the validate method returned true and thus the user input
        is valid.
        """
        self._name = self._name_entry.get()
        self._paths = [selector.get() for selector in self._path_selectors]
        self._format = self._format_selector.get()

    def validate(self):
        """
        proofs if the current user input is valid or not.
        The _name of the dataset can only be set once.
        """

        for path_selector in self._path_selectors:
            path = path_selector.get()
            if not os.path.exists(path):
                path_selector.set("")
                showerror(message=EnglishTexts.INVALID_FILE_PATH.value.format(path))
                self._valid_input = False
                return False

        self._valid_input = True
        return True

    def get_paths(self):
        """
        returns the path selected by the user
        """
        return self._paths

    def get_name(self):
        """
        returns the _name selected by the user
        """
        return self._name

    def get_format(self):
        """
        returns the format selected by the user
        """
        return self._format

    def is_valid(self):
        """
        returns true if the user input to the dialog was valid. Otherwise false will be returned.
        """
        return self._valid_input
