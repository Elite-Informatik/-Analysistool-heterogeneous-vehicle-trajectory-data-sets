import tkinter as tk
from tkinter import ACTIVE
from tkinter import LEFT
from tkinter.messagebox import showerror
from typing import List

from src.data_transfer.record.setting_record import SettingRecord
from src.view.user_interface.selection.selection_frame import SelectionFrame
from src.view.user_interface.static_windows.window import Window
from src.view.user_interface.ui_util.texts import EnglishTexts


class SelectionWindow(Window):
    """
    This window displays a list of setting records and provides the (by the user) modified setting records.
    """

    def __init__(self, setting_records: List[SettingRecord], func_ok, title: str = ""):
        """
        creates a new SelectionWindow
        :param setting_records:     the setting records
        :param func_ok:             the method executed when user entered valid input confirmed
        """
        super().__init__()
        self._window = tk.Tk()
        self._window.title(title)
        self._func_ok = func_ok
        self._selection_frame = SelectionFrame(setting_records)
        self._new_setting_records: List[SettingRecord] = []
        self._valid_input = False
        self.__build()

    def run(self):

        self._window.mainloop()

    def destroy(self):

        self._window.destroy()

    def __build(self):
        """
        builds the window
        """
        self._base_frame = tk.Frame(master=self._window)
        self._selection_frame.build(self._base_frame).pack()
        box_frame = tk.Frame(self._base_frame)
        ok_btn = tk.Button(box_frame, text=EnglishTexts.OK_BTN_NAME.value, width=10, command=self.__on_ok,
                           default=ACTIVE)
        ok_btn.pack(side=LEFT, padx=5, pady=5)
        cancel_btn = tk.Button(box_frame, text=EnglishTexts.CANCEL_BTN_NAME.value, width=10, command=self.__on_cancel)
        cancel_btn.pack(side=LEFT, padx=5, pady=5)
        box_frame.pack()
        self._base_frame.pack()

    def __on_ok(self):
        """
        executed when user presses ok
        """
        if self.__validate():
            self._selection_frame.collect_new_setting_records()
            self.destroy()
            self._func_ok()
        else:
            showerror(EnglishTexts.ERROR_INVALID_INPUT.value, EnglishTexts.INSTRUCTION_INVALID_INPUT.value)
            pass

    def __on_cancel(self):
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

        return self._selection_frame.new_setting_records

    @property
    def valid_input(self) -> bool:

        return self._selection_frame.valid_input
