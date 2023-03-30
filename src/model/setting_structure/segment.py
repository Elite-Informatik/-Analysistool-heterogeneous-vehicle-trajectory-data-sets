from typing import List

from src.data_transfer.content.settings_enum import SettingsEnum
from src.data_transfer.record.selection_record import SelectionRecord
from src.data_transfer.record.settings_record import SegmentRecord
from src.model.setting_structure.setting import Setting


class Segment:
    """
    Represents a segment in a Page, consisting of a collection of Settings.
    """

    def __init__(self, identifier: SettingsEnum, name: str, settings: List[Setting]):
        """
        Initialize a new Segment with the given _name and list of Settings.

        :param name: String representing the _name of the segment.
        :param settings: List of Setting objects.
        """
        self._identifier: SettingsEnum = identifier

        self._name: str = name
        self._settings: List[Setting] = settings.copy()

    @classmethod
    def from_record(cls, record: SegmentRecord):
        """
        Initialize a new Segment from a SegmentRecord.

        :param record: SegmentRecord object to be converted into a Segment.
        :return: Segment object created from the given SegmentRecord.
        """
        return cls(identifier=record.identifier, name=record.name,
                   settings=list(Setting.from_record(setting_record) for setting_record in record.setting_records))

    def add_setting(self, setting: Setting) -> bool:
        """
        Adds a new Setting to the Segment, if it does not already exist.

        :param setting: Setting to be added.
        :return: True if the Setting was added successfully, False otherwise.
        """
        if setting in self._settings:
            return False
        self._settings.append(setting)
        return True

    def get_settings(self) -> List[Setting]:
        """
        Retrieve a copy of the list of Settings in the Segment.

        :return: List of Setting objects.
        """
        return self._settings.copy()

    def get_name(self):
        """
        Retrieve the _name of the Segment.

        :return: String representing the _name of the Segment.
        """
        return self._name

    def get_record(self):
        """
        Creates an immutable snapshot of the current state of the Segment as a SegmentRecord.

        :return: The SegmentRecord mirroring the current state of the class.
        """
        return SegmentRecord(_identifier=self._identifier,
                             _settings=tuple(i.get_setting_record() for i in self._settings), _name=self._name)

    def get_identifier(self) -> SettingsEnum:
        """
        Getter for the segment individual identifier

        :return: the identifier
        :rtype: str
        """
        return self._identifier

    def create_setting(self, identifier: SettingsEnum, name: str, setting: SelectionRecord) -> bool:
        """
        Creates setting in the segment based on an identifier, a name and a selection content

        :param identifier: The identifier for the new setting
        :type identifier: str
        :param name: The name of the new setting
        :type name: str
        :param setting: The selection that represents the setting
        :type setting: SelectionRecord

        :return: If the setting was created
        :rtype: bool
        """
        for setting in self._settings:
            if setting.get_identifier() == identifier:
                return False
        self._settings.append(Setting(identifier=identifier, selection=setting, name=name))

    def load_from_dict(self, dictionary: dict):
        """
        Loads the content from a dictionary

        :param dictionary: The dictionary to load from
        :type dictionary: dict
        """
        for setting in self._settings:
            setting.load_from_dict(dictionary)

    def export_to_dict(self, dictionary: dict):
        """
        Export the content to a dictionary

        :param dictionary: The dictionary to export to
        :type dictionary: dict
        """
        for setting in self._settings:
            setting.export_to_dict(dictionary)
