import tkinter as tk
from tkinter import LEFT

from src.data_transfer.record.setting_record import SettingRecord
from src.view.user_interface.selection.selection_unit import SelectionUnit


class BoolSelectionUnit(SelectionUnit):
    """
    represents the visualisation of a setting record of a boolean option
    """

    def __init__(self, selection: SettingRecord):
        super().__init__(selection)
        self._checkbox = None

    def build(self, master) -> tk.Widget:
        body_frame = tk.Frame(master=master)
        context = self._build_context(master=body_frame, text=self._shown_selection.context)
        context.pack(side=LEFT, padx=5, pady=5, anchor="w")

        self._checkbox = tk.BooleanVar(master=body_frame, value=self._shown_selection.selection.selected[0])
        checkbox = tk.Checkbutton(body_frame, anchor="w", variable=self._checkbox, onvalue=1, offvalue=0, )
        checkbox.pack(after=context, fill="x", padx=5, expand=True, side=LEFT)

        return body_frame

    def validate(self) -> bool:
        return True

    def get_chosen_setting_record(self) -> SettingRecord:
        new_selection = self._shown_selection.selection.set_selected([self._checkbox.get()])
        return SettingRecord(self._shown_selection.context, new_selection, _identifier=self._shown_selection.identifier)
