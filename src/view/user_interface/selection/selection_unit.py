import tkinter as tk
from abc import ABC
from abc import abstractmethod
from typing import List

from tktooltip import ToolTip

from src.data_transfer.record.setting_record import SettingRecord


class SelectionUnit(ABC):
    """
    represents the visualisation of a setting record
    """

    def __init__(self, selection: SettingRecord):
        """
        creates a new selection unit
        :param selection: the selection to visualize
        """
        self._shown_selection: SettingRecord = selection
        self._callback_functions: List[callable] = []

    @abstractmethod
    def build(self, master) -> tk.Widget:
        """
        creates the frame containing the visualization of the setting record
        :param master: the master
        :return:       the new frame
        """
        pass

    def _build_context(self, master, text) -> tk.Label:
        context =  tk.Label(master=master, text=text, width=40, anchor="nw")
        tip = self._shown_selection.tip
        if tip is not None:
            ToolTip(widget=context, msg=tip, delay=0.3)
        return context

    @abstractmethod
    def validate(self) -> bool:
        """
        checks whether input is a valid option for the selection
        :return: whether input is valid
        """
        pass

    @abstractmethod
    def get_chosen_setting_record(self) -> SettingRecord:
        """
        gets the setting record containing the new modified selections
        :return: the new setting record
        """
        pass

    def add_callback(self, callback_function: callable):
        """
        Adds a callback Function to the Selection Unit. The function gets always executed when the selected
        item has changed.
        """
        self._callback_functions.append(callback_function)

    def execute_callbacks(self):
        """
        Executes all callback functions.
        """
        for callback in self._callback_functions:
            callback()