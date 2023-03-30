import tkinter as tk
from typing import List

from src.data_transfer.record.setting_record import SettingRecord
from src.view.user_interface.selection.selection_unit import SelectionUnit
from src.view.user_interface.selection.selection_unit_factory import SelectionUnitFactory


class SelectionFrame:
    """
    represents a frame that displays a list of setting records and provides the (by the user) modified setting records.
    """

    def __init__(self, setting_records: List[SettingRecord]):
        """
        creates a new SelectionFrame
        :param setting_records: the setting records
        """
        self._valid_input: bool = None
        self._base_frame: tk.Frame = None
        factory = SelectionUnitFactory()
        self._selection_units: List[SelectionUnit] = [factory.create_selection_unit(e) for e in setting_records]
        self._new_setting_records: List[SettingRecord] = []

    def build(self, master) -> tk.Frame:
        """
        builds the selection frame
        :param master:  the master of the selection frame
        :return:        the selection frame
        """
        self._base_frame = tk.Frame(master)
        for unit in self._selection_units:
            unit_frame = unit.build(self._base_frame)
            unit_frame.grid(sticky="nsew", padx=5, pady=5)
        return self._base_frame

    def destroy(self):
        self._base_frame.destroy()

    def validate(self) -> bool:
        """
        checks whether the input is valid
        :return: whether the input is valid
        """
        for unit in self._selection_units:
            if not unit.validate():
                return False
        self._valid_input = True
        return self._valid_input

    def collect_new_setting_records(self) -> List[SettingRecord]:
        """
        collects the new (by the user modified) setting records
        :return:    the new setting records
        """
        new_setting_records: List[SettingRecord] = []
        for unit in self._selection_units:
            new_setting_records.append(unit.get_chosen_setting_record())
        self._new_setting_records = new_setting_records
        return self._new_setting_records

    @property
    def new_setting_records(self) -> List[SettingRecord]:

        return self._new_setting_records

    @property
    def valid_input(self) -> bool:

        return self._valid_input
