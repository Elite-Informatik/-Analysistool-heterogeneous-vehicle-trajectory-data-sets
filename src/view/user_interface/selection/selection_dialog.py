from tkinter.messagebox import showerror
from tkinter.simpledialog import Dialog
from typing import List

from src.data_transfer.record.setting_record import SettingRecord
from src.view.user_interface.selection.selection_frame import SelectionFrame
from src.view.user_interface.ui_util.texts import EnglishTexts


class SelectionDialog(Dialog):
    """
    This window displays a list of setting records and provides the (by the user) modified setting records.
    """

    def __init__(self, setting_records: List[SettingRecord]):
        """
        creates a new SelectionWindow
        :param setting_records:     the setting records
        """
        self._selection_frame = SelectionFrame(setting_records)
        self._new_setting_records: List[SettingRecord] = []
        super().__init__(parent=None, title=EnglishTexts.USER_REQUEST_DIALOG_NAME.value)

    def body(self, master) -> None:
        self._selection_frame.build(self).pack()

    def ok(self):
        """
        executed when user presses ok
        """
        if self.__validate():
            self._selection_frame.collect_new_setting_records()
            self.destroy()
        else:
            showerror(EnglishTexts.ERROR_INVALID_INPUT.value, EnglishTexts.INSTRUCTION_INVALID_INPUT.value)
            pass

    def cancel(self):
        """
        executed when user presses cancel
        :return:
        """
        self.destroy()

    def __validate(self) -> bool:
        """
        checks whether user input is valid
        :return: whether user input is valid
        """
        self._selection_frame.validate()
        return self._selection_frame.valid_input

    @property
    def new_setting_records(self) -> List[SettingRecord]:
        """
        the new by the user modified setting record
        """
        return self._selection_frame.new_setting_records

    @property
    def valid_input(self) -> bool:
        """
        whether the input was valid
        """
        return self._selection_frame.valid_input
