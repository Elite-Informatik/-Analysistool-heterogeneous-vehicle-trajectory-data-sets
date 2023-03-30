import tkinter as tk

from src.data_transfer.record.setting_record import SettingRecord
from src.view.user_interface.selection.selection_unit import SelectionUnit


class NumberIntervalSelectionUnit(SelectionUnit):
    """
    represents the visualisation of a setting record of an interval option expecting numbers
    """

    def __init__(self, selection: SettingRecord):
        super().__init__(selection)
        start_value = self._shown_selection.selection.selected[0][0]
        end_value = self._shown_selection.selection.selected[0][1]
        self._start_selector = tk.Variable(value=start_value)
        self._end_selector = tk.Variable(value=end_value)

    def build(self, master) -> tk.Widget:
        base_frame = tk.Frame(master=master)

        start_value_entry = tk.Entry(master=base_frame, textvariable=self._start_selector)
        start_value_entry.grid(column=0, row=0)

        tk.Label(master=base_frame, text="to").grid(column=1, row=0)

        end_value_entry = tk.Entry(master=base_frame, textvariable=self._end_selector)
        end_value_entry.grid(column=2, row=0)

        return base_frame

    def validate(self) -> bool:
        start_value = float(self._start_selector.get())
        end_value = float(self._end_selector.get())

        return self._shown_selection.selection.option.is_valid(option=[start_value, end_value])

    def get_chosen_setting_record(self) -> SettingRecord:
        start_value = float(self._start_selector.get())
        end_value = float(self._end_selector.get())
        new_selection = self._shown_selection.selection.set_selected([[start_value, end_value]])
        return SettingRecord(_context=self._shown_selection.context, _selection=new_selection,
                             _identifier=self._shown_selection.identifier)
