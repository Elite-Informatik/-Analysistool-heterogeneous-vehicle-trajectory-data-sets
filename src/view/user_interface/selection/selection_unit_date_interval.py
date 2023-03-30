import re
import tkinter as tk
from datetime import datetime
from tkinter.messagebox import showerror

from src.data_transfer.record.setting_record import SettingRecord
from src.view.user_interface.selection.selection_unit import SelectionUnit


class DateIntervalSelectionUnit(SelectionUnit):
    """
    represents the visualisation of a setting record with interval option expecting dates
    """
    DATE_FORMAT_VIEW = "%d-%m-%Y"
    DATE_FORMAT_DATATRANSFER = "%Y-%m-%d"
    DATE_REGEX = re.compile("\d{1,2}-\d{1,2}-\d{4}")
    DATE_FORMAT_DISPLAYED = "DD-MM-YYYY"

    def __init__(self, selection: SettingRecord):
        super().__init__(selection)
        start_date = self._convert_datatransfer_format_to_view_format(self._shown_selection.selection.selected[0][0])
        end_date = self._convert_datatransfer_format_to_view_format(self._shown_selection.selection.selected[0][1])

        self._start_date_selector = tk.StringVar(value=start_date)
        self._end_date_selector = tk.StringVar(value=end_date)

    def build(self, master) -> tk.Widget:
        base_frame = tk.Frame(master=master)

        start_date_entry = tk.Entry(master=base_frame, textvariable=self._start_date_selector)
        start_date_entry.grid(column=0, row=0)

        tk.Label(master=base_frame, text="to").grid(column=1, row=0)

        end_date_entry = tk.Entry(master=base_frame, textvariable=self._end_date_selector)
        end_date_entry.grid(column=2, row=0)

        return base_frame

    def validate(self) -> bool:
        """
        proofs the validity of the user input.
        the dates must match the format DD-MM-YYYY and the start date must be before the end date.
        The validity of the range is checked by the option itself.
        :return: True if the user input is valid, False otherwise
        """
        start_date = self._start_date_selector.get()
        end_date = self._end_date_selector.get()
        start_date = start_date.strip()
        if not self.DATE_REGEX.match(start_date):
            showerror(message=f"Start date has invalid format. Date must be of format: {self.DATE_FORMAT_DISPLAYED}")
            return False
        end_date = end_date.strip()
        if not self.DATE_REGEX.match(end_date):
            showerror(message=f"End date has invalid format. Date must be of format: {self.DATE_FORMAT_DISPLAYED}")
            return False
        start_date = self._convert_view_format_to_datatransfer_format(start_date)
        end_date = self._convert_view_format_to_datatransfer_format(end_date)
        if not self._shown_selection.selection.option.is_valid([start_date, end_date]):
            showerror(message=f"Invalid date interval")
            return False
        return True

    def get_chosen_setting_record(self) -> SettingRecord:
        """
        This method should only be used when validate returns True.
        :return: the setting record with the user input
        """
        start_date = self._convert_view_format_to_datatransfer_format(self._start_date_selector.get())
        end_date = self._convert_view_format_to_datatransfer_format(self._end_date_selector.get())
        new_selection = self._shown_selection.selection.set_selected(selected=[[start_date, end_date]])
        return SettingRecord(_context=self._shown_selection.context, _selection=new_selection,
                             _identifier=self._shown_selection.identifier)

    def _convert_view_format_to_datatransfer_format(self, date_string: str) -> str:
        """
        This method converts the date format from the view format to the format used for data transfer.
        """
        date_time = datetime.strptime(date_string, self.DATE_FORMAT_VIEW)
        return datetime.strftime(date_time, self.DATE_FORMAT_DATATRANSFER)

    def _convert_datatransfer_format_to_view_format(self, data_string: str) -> str:
        """
        This method converts the date format from the format used for data transfer to the view format.
        """
        date_time = datetime.strptime(data_string, self.DATE_FORMAT_DATATRANSFER)
        return datetime.strftime(date_time, self.DATE_FORMAT_VIEW)
