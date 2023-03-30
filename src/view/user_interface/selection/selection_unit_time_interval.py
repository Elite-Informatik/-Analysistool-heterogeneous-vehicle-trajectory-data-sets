import re
import tkinter as tk
from tkinter.messagebox import showerror

from src.data_transfer.record.setting_record import SettingRecord
from src.view.user_interface.selection.selection_unit import SelectionUnit


class TimeIntervalSelectionUnit(SelectionUnit):
    """
    represents the visualisation of a setting record of an interval option expecting times
    """
    TIME_FORMAT = "%H:%M:%S"
    TIME_REGEX = re.compile("^\d{1,2}:\d{1,2}:\d{1,2}$")
    TIME_FORMAT_DISPLAYED = "HH:MM:SS"

    def __init__(self, selection: SettingRecord):
        super().__init__(selection)
        self._start_time_selector = tk.StringVar(value=selection.selection.selected[0][0])
        self._end_time_selector = tk.StringVar(value=selection.selection.selected[0][1])

    def build(self, master) -> tk.Widget:
        base_frame = tk.Frame(master=master)

        start_date_entry = tk.Entry(master=base_frame, textvariable=self._start_time_selector)
        start_date_entry.grid(column=0, row=0)

        tk.Label(master=base_frame, text="to").grid(column=1, row=0)

        end_date_entry = tk.Entry(master=base_frame, textvariable=self._end_time_selector)
        end_date_entry.grid(column=2, row=0)

        return base_frame

    def validate(self) -> bool:
        """
        validates the time interval
        The time is valid if it matches the format HH:MM:SS and the start time is before the end time
        The validity of the range is checked by the option itself.
        :return: True if the time interval is valid, False otherwise
        """
        start_date = self._start_time_selector.get()
        end_date = self._end_time_selector.get()
        start_date = start_date.strip()
        if not self.TIME_REGEX.match(start_date):
            showerror(message=f"start time does not match valid format: {self.TIME_FORMAT_DISPLAYED}")
            return False
        end_date = end_date.strip()
        if not self.TIME_REGEX.match(end_date):
            showerror(message=f"end time does not match valid format: {self.TIME_FORMAT_DISPLAYED}")
            return False
        if not self._shown_selection.selection.option.is_valid(option=[start_date, end_date]):
            showerror(message=f"time interval is not valid")
            return False
        return True

    def get_chosen_setting_record(self) -> SettingRecord:
        """
        returns the setting record with the selected time interval
        """
        selected = [self._start_time_selector.get(), self._end_time_selector.get()]
        new_selection = self._shown_selection.selection.set_selected(selected=[selected])
        return SettingRecord(_context=self._shown_selection.context, _selection=new_selection,
                             _identifier=self._shown_selection.identifier)
