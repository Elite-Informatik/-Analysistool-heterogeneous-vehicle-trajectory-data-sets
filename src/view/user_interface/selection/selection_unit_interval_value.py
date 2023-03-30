import tkinter as tk
from tkinter import END
from tkinter import LEFT
from typing import List
from typing import Optional

from src.data_transfer.record.setting_record import SettingRecord
from src.view.user_interface.selection import selection_util
from src.view.user_interface.selection.selection_unit import SelectionUnit


class IntervalValueSelectionUnit(SelectionUnit):
    """
    represents the visualisation of a setting record of an interval value option
    """

    SEPARATION = ','

    def __init__(self, selection: SettingRecord):
        super().__init__(selection)
        self._value_entry = None
        self._value_selector = tk.StringVar()

    def build(self, master) -> tk.Widget:

        body_frame = tk.Frame(master=master)
        context = self._build_context(master=body_frame, text=self._shown_selection.context)
        context.pack(side=LEFT, padx=5, pady=5, anchor="nw")

        amount_range: range = self._shown_selection.selection.possible_selection_amount
        interval: List = self._shown_selection.selection.option.get_option()
        # instruction for user: nr of possible entries
        instruction = selection_util.create_interval_instruction_label(body_frame, amount_range.start,
                                                                       amount_range.stop, interval[0], interval[1])
        instruction.pack()

        default_entry = self.SEPARATION.join(map(str, self._shown_selection.selection.selected))
        self._value_entry = tk.Entry(master=body_frame, textvariable=self._value_selector)
        self._value_entry.insert(END, default_entry)
        self._value_entry.pack(after=context, fill="x", padx=5, expand=True)
        return body_frame

    def __split_input_to_numbers(self, input: str) -> Optional[List[float]]:
        entry_str: List[str] = input.split(sep=self.SEPARATION)
        entry_int: List[float] = []
        for e in entry_str:
            entry_int.append(float(e))
        return entry_int

    def __are_numbers(self, input: List[str]) -> bool:
        for i in input:
            try:
                float(i)
                return True
            except ValueError:
                return False

    def validate(self) -> bool:
        if not self.__are_numbers(self._value_selector.get().split(sep=self.SEPARATION)):
            return False
        entry_ints = self.__split_input_to_numbers(self._value_selector.get())
        if not len(entry_ints) in self._shown_selection.selection.possible_selection_amount:
            return False
        for e in entry_ints:
            if not self._shown_selection.selection.option.is_valid(e):
                return False
        return True

    def get_chosen_setting_record(self) -> SettingRecord:

        entry_ints = self.__split_input_to_numbers(self._value_selector.get())
        new_selection = self._shown_selection.selection.set_selected(entry_ints)
        return SettingRecord(self._shown_selection.context, new_selection,
                             _identifier=self._shown_selection.identifier)
