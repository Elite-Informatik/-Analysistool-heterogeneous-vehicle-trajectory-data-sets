import tkinter as tk
from typing import Tuple

from src.data_transfer.record import SegmentRecord
from src.data_transfer.record.setting_record import SettingRecord
from src.view.controller_communication.controller_communication import ControllerCommunication
from src.view.user_interface.selection.selection_frame import SelectionFrame


class SettingsSegment:
    """
    Represents a segment in a settings page. Acts like a UiElement with the build and destroy methods.
    But it is created dynamically and does not need to be notified about any events. Thereby the class
    does not inherit from UiElement.
    """

    def __init__(self, segment: SegmentRecord, controller_communication: ControllerCommunication):
        self._controller_communication = controller_communication

        self._segment: SegmentRecord = segment
        self._settings: Tuple[SettingRecord, ...] = segment.setting_records
        self._base_frame: SelectionFrame = None

    def build(self, master: tk.Widget) -> tk.Widget:
        """
        See documentation of the UiElement class.
        """
        self._base_frame = SelectionFrame(setting_records=list(self._settings))
        return self._base_frame.build(master)

    def destroy(self):
        """
        See documentation of the UiElement class.
        """
        self._base_frame.destroy()

    def to_segment(self):
        """
        Converts the view to a segment record.
        """
        new_setting_records = self._base_frame.collect_new_setting_records()
        new_segment_record = SegmentRecord(_settings=tuple(new_setting_records),
                                           _identifier=self._segment.identifier,
                                           _name=self._segment.name)
        self._segment = new_segment_record
        # for setting_record in new_setting_records:
        # self._segment = self._segment.change(identifier=setting_record.identifier, value=setting_record.selection)
        return self._segment

    def validate(self) -> bool:
        """
        proofs if the user input to that segment is valid
        """
        return self._base_frame.validate()
