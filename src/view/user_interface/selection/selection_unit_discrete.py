import tkinter as tk
from tkinter import LEFT
from typing import List

from src.data_transfer.record.setting_record import SettingRecord
from src.view.user_interface.selection.selection_unit import SelectionUnit
from src.view.user_interface.ui_util.texts import EnglishTexts
from src.view.user_interface.selection import selection_util


class DiscreteSelectionUnit(SelectionUnit):
    """
    represents the visualisation of a setting record with discrete option
    """

    def __init__(self, selection: SettingRecord):
        super().__init__(selection)
        self._body_frame = None
        self._options = None
        self._value_listbox = None
        self._selected_values: List = []
        self._callbacks: List[callable] = []

    def build(self, master) -> tk.Widget:

        self._body_frame = tk.Frame(master=master)
        context = self._build_context(self._body_frame, self._shown_selection.context)
        context.pack(side=LEFT, padx=5, pady=5, anchor="nw")

        amount_range: range = self._shown_selection.selection.possible_selection_amount
        instruction = selection_util.create_discrete_instruction_label(self._body_frame, amount_range.start, amount_range.stop)
        instruction.pack()

        self._options: List = self._shown_selection.selection.option.get_option()
        default_values = self._shown_selection.selection.selected

        if len(self._shown_selection.selection.possible_selection_amount) == 1:
            select_mode = tk.SINGLE
        else:
            select_mode = tk.MULTIPLE
        self._value_listbox = tk.Listbox(master=self._body_frame, height=6, selectmode=select_mode, exportselection=0)

        for i, option in enumerate(self._options):
            if not isinstance(option, str):
                self._value_listbox.insert(i, option.__repr__())
            else:
                self._value_listbox.insert(i, option)
            if option in default_values:
                self._value_listbox.select_set(i)

        self._value_listbox.bind("<<ListboxSelect>>", lambda event: self.process_list_select(event))
        self.set_selected()

        self._value_listbox.pack(after=context, fill="x", padx=5, expand=True)

        return self._body_frame

    def process_list_select(self, event=None):
        self.set_selected()
        self.execute_callbacks()

    def set_selected(self):
        selected_indices = self._value_listbox.curselection()
        self._selected_values = [self._options[i] for i in selected_indices]

    def destroy(self):
        self._body_frame.destroy()

    def validate(self) -> bool:
        if not len(self._selected_values) in self._shown_selection.selection.possible_selection_amount:
            return False
        for e in self._selected_values:
            if not self._shown_selection.selection.option.is_valid(e):
                return False
        return True

    def get_chosen_setting_record(self) -> SettingRecord:
        new_selection = self._shown_selection.selection.set_selected(self._selected_values)
        return SettingRecord(_context=self._shown_selection.context, _selection=new_selection,
                             _identifier=self._shown_selection.identifier)
