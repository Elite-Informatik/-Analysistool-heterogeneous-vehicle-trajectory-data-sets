import tkinter as tk
from tkinter.simpledialog import Dialog
from typing import Dict
from uuid import UUID

from src.data_transfer.record.data_set_record import DatasetRecord
from src.view.user_interface.ui_util.texts import EnglishTexts


class OpenDatasetDialog(Dialog):
    """
    This class defines a dialog that is used to let the user select one of the datasets
    that has already been processed by the application and can be used. This class inherits from the
    Dialog class and overrides its template methods to define a new dialog.
    """

    def __init__(self, datasets: Dict[UUID, DatasetRecord]):
        """
        The dialog will be immediately displayed on the screen when the constructor is called.
        """
        # names of datasets must be unique otherwise error could occur
        self._clicked = None
        self._dropdown = None
        self.options = {}
        for dataset_id, dataset in datasets.items():
            self.options.update({dataset.name: dataset_id})

        self._selected_id: UUID = None
        self._is_valid = False

        super().__init__(parent=None, title=EnglishTexts.OPEN_DATASET_DIALOG_NAME.value)

    def body(self, master: tk.Frame):
        """
        Defines how the body of the dialog should look like
        """
        self._clicked = tk.StringVar()
        self._clicked.set("select a dataset")

        self._dropdown = tk.OptionMenu(master, self._clicked, *self.options)
        self._dropdown.pack()

    def apply(self):
        """
        sets the variables the hold the user input to the current user input in the tk.OptionMenu.
        This method is called when the user input is valid. The user input can now be read from the dialog instace.
        """
        self._selected_id = self.options[self._clicked.get()]

    def validate(self) -> bool:
        """
        proofs if the current user input is valid. returns true if so, otherwise false
        """
        if self._clicked.get() in self.options.keys():
            self._is_valid = True
            return True
        else:
            self._is_valid = False
            return False

    def is_valid(self) -> bool:
        """
        this method gets called after the dialog has been closed and the user input has been made. It can be used
        to proof if the input given by the user was valid or if the user input was invalid
        """
        return self._is_valid

    def get_id_selected(self) -> UUID:
        """
        returns the id that was selected by the user.
        """
        return self._selected_id
