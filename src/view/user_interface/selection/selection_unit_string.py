import tkinter as tk
from tkinter import END
from tkinter import LEFT

from src.data_transfer.record.setting_record import SettingRecord
from src.view.user_interface.selection.selection_unit import SelectionUnit


class StringSelectionUnit(SelectionUnit):
    """
    represents the visualisation of a setting record of a string option
    """

    def __init__(self, selection: SettingRecord):
        super().__init__(selection)
        self._string_entry = None
        self._string_var = tk.StringVar()

    def build(self, master) -> tk.Widget:
        body_frame = tk.Frame(master=master)
        context = self._build_context(body_frame, self._shown_selection.context)
        context.pack(side=LEFT, padx=5, pady=5, anchor="nw")
        self._string_entry = tk.Entry(master=body_frame, textvariable=self._string_var)
        self._string_entry.insert(END, self._shown_selection.selection.selected)
        self._string_entry.pack(after=context, fill="x", padx=5, expand=True)
        return body_frame

    def validate(self) -> bool:
        return self._shown_selection.selection.option.is_valid(self._string_var.get())

    def get_chosen_setting_record(self) -> SettingRecord:
        new_selection = self._shown_selection.selection.set_selected([self._string_var.get()])
        return SettingRecord(self._shown_selection.context, new_selection,
                             _identifier=self._shown_selection.identifier)
