import tkinter as tk
from tkinter import ACTIVE
from tkinter import LEFT
from tkinter.messagebox import showerror
from tkinter.simpledialog import Dialog
from typing import Dict
from typing import List
from typing import Optional

from src.data_transfer.record import AnalysisTypeRecord
from src.view.user_interface.ui_util.texts import EnglishTexts


class CreateAnalysisDialog(Dialog):
    """
    represents a dialog to create a new analysis.
    """

    def __init__(self, analysis_types: List[AnalysisTypeRecord]):
        """
        creates a new CreateAnalysisDialog.
        The dialog will be immediately displayed on the screen when the constructor is called.
        :param analysis_types:  all available analysis types
        """
        self._clicked = None
        self._analysis_types_options: Dict[str, AnalysisTypeRecord] = {}
        for a in analysis_types:
            self._analysis_types_options[a.name] = a
        self._selected_analysis_type: Optional[AnalysisTypeRecord] = None
        self._valid_input = False
        super().__init__(parent=None, title=EnglishTexts.CREATE_ANALYSIS_DIALOG_TITLE.value)

    def body(self, master):

        body_frame = tk.Frame(master=master)
        # body_frame.grid_propagate(False)
        select_type_instruction = tk.Label(master=body_frame, text=EnglishTexts.INSTRUCTION_SELECT_ANALYSIS_TYPE.value,
                                           anchor="w")
        select_type_instruction.grid(row=0, column=0, sticky="w", pady=5, padx=5)
        self._clicked = tk.StringVar()
        self._clicked.set("analysis type")
        analysis_type_dropdown = tk.OptionMenu(body_frame, self._clicked, *self._analysis_types_options.keys())
        analysis_type_dropdown.grid(row=0, column=1, sticky="w", padx=5, pady=5)

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

    def ok(self):

        if self.validate(self._clicked.get()):
            self._selected_analysis_type = self._analysis_types_options[self._clicked.get()]
            self.destroy()
        else:
            showerror(EnglishTexts.ERROR_INVALID_INPUT.value, EnglishTexts.INSTRUCTION_INVALID_INPUT.value)
            pass

    def cancel(self):

        self.destroy()

    def validate(self, selected: str) -> bool:

        self._valid_input = self._analysis_types_options.get(selected) is not None
        return self._valid_input

    @property
    def selected_analysis_type(self) -> AnalysisTypeRecord:

        return self._selected_analysis_type

    @property
    def valid_input(self) -> bool:

        return self._valid_input
