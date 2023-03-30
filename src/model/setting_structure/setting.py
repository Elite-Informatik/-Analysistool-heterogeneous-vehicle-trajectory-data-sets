from typing import List, Optional
from typing import Type

from src.data_transfer.record.selection_record import SelectionRecord
from src.data_transfer.record.setting_record import SettingRecord
from src.data_transfer.selection.discrete_option import DiscreteOption
from src.data_transfer.selection.interval_value_option import IntervalValueOption
from src.data_transfer.selection.string_option import StringOption

from src.data_transfer.content.settings_enum import SettingsEnum


class Setting:
    """
    This class represents a setting with a set of option and a default selected option
    """
    EXPORTABLE_SETTING_TYPES: List[Type] = [str, int, float]

    def __init__(self, selection: SelectionRecord, name: str, identifier: SettingsEnum = SettingsEnum.DEF_SETTING,
                 tip: Optional[str] = None):
        """
        Initialize a Setting instance with a set of option and a default selected option

        :param selection: The set of option for this setting
        :param name: The _name of the setting
        :raise ValueError: If the default_selected argument is not a valid option of the option set
        """
        if len(selection.selected) != 1:
            raise ValueError("The selection chosen has not got a default length of 1")
        self._identifier: SettingsEnum = identifier
        self._options = selection.option
        self._type = selection.type
        self._name = name
        self._tip: Optional[str] = tip
        # if not self._option.is_valid(selection.selected):
        #    raise ValueError(f"The supplied default_selected: {selection.selected} argument is not a valid option of "
        #                     f"the optionSet {option.get_option_type()} with option: {option.get_option()}")
        self._selected = selection.selected[0]

    @classmethod
    def boolean_setting(cls, name: str, identifier: SettingsEnum = SettingsEnum.DEF_SETTING, tip: Optional[str] = None):
        """
        Creates a boolean setting
        """
        selection = SelectionRecord.bool()
        return cls(selection=selection, name=name, identifier=identifier, tip=tip)

    @classmethod
    def from_list(cls, name: str, option_list: List, standard, identifier: SettingsEnum = SettingsEnum.DEF_SETTING,
                  tip: Optional[str] = None):
        """
        Creates a setting from an option list

        :param identifier: the identifier of the setting
        :type identifier: str
        :param name: the name of the setting
        :type name: str
        :param option_list: the list of selectable options
        :type option_list: List
        :param standard: the default selected
        """
        if len(option_list) <= 0:
            raise ValueError
        option_set = DiscreteOption(option_list.copy())
        selected_list: List = list()
        selected_list.append(standard)
        selection_record = SelectionRecord(selected_list, option_set, range(1, 2))
        return cls(identifier=identifier, selection=selection_record, name=name, tip=tip)

    @classmethod
    def from_interval(cls, name: str, standard: float, minimum: float, maximum: float,
                      identifier: SettingsEnum = SettingsEnum.DEF_SETTING, tip: Optional[str] = None):
        """
        Creates a setting from a given min and maximum

        :param identifier: the identifier of the setting
        :type identifier: str
        :param name: the name of the setting
        :type name: str
        :param standard: the default selected
        :type standard: float
        :param minimum: the minimum selectable
        :type minimum: float
        :param maximum: the maximum selectable
        :type maximum: float
        """
        if standard < minimum or standard > maximum:
            raise ValueError
        option_set = IntervalValueOption(minimum, maximum)
        selection_record = SelectionRecord([standard], option_set, range(1, 2))
        return cls(identifier=identifier, selection=selection_record, name=name, tip=tip)

    @classmethod
    def from_string(cls, name: str, regex: str, standard: str, identifier: SettingsEnum = SettingsEnum.DEF_SETTING,
                    tip: Optional[str] = None):
        """
        Creates a setting from a given regex

        :param identifier: the identifier of the setting
        :type identifier: str
        :param name: the name of the setting
        :type name: str
        :param standard: the default selected
        :type standard: str
        :param regex: the regex that the selections have to fit
        :type regex: str
        """
        string_option: StringOption = StringOption(valid_string=regex)
        selection_record = SelectionRecord([standard], string_option, range(1, 2))
        return cls(identifier=identifier, selection=selection_record, name=name, tip=tip)

    @classmethod
    def from_record(cls, record: SettingRecord):
        """
        Initialize a new Setting from a SettingRecord.

        :param record: SettingRecord object to be converted into a Segment.
        :return: Setting object created from the given SettingRecord.
        """
        if len(record.selection.selected) != 1:
            raise ValueError(f"An incorrect amount of selected arguments were given. "
                             f"Expected 1, but given: {record.selection.selected}")
        return cls(identifier=record.identifier, selection=record.selection, name=record.context, tip=record.tip)

    def get_selected(self):
        """
        Get the currently selected option

        :return: The currently selected option
        """
        return self._selected

    def get_options(self) -> []:
        """
        Get the set of option for this setting

        :return: The set of option for this setting
        """
        return self._options.get_options()

    def set_selected(self, option) -> bool:
        """
        Set the selected option

        :param option: The option to set as selected
        :return: True if the option is valid and is set as selected, False otherwise
        """
        if not self._options.is_valid(option):
            return False
        self._selected = option
        return True

    def get_setting_record(self) -> SettingRecord:
        """
        Creates an immutable snapshot of the current state of the setting as a SettingRecord

        :return: The SettingRecord mirroring the current state of the class
        """
        return SettingRecord(self._name,
                             SelectionRecord(
                                 [self._selected],
                                  self._options),
                                  self._identifier,
                                  _tip=self._tip)

    def get_identifier(self) -> SettingsEnum:
        """
        Getter for the identifier

        :return: the identifier
        :rtype: str
        """
        return self._identifier

    def load_from_dict(self, dictionary: dict):
        """
        Loads the content from a dictionary

        :param dictionary: The dictionary to load from
        :type dictionary: dict
        """
        if self._type not in self.EXPORTABLE_SETTING_TYPES:
            return
        if self._identifier.value not in dictionary.keys():
            return
        self._selected = dictionary[self._identifier.value]

    def export_to_dict(self, dictionary: dict):
        """
        Export the content to a dictionary

        :param dictionary: The dictionary to export to
        :type dictionary: dict
        """
        if self._type not in self.EXPORTABLE_SETTING_TYPES:
            return
        dictionary[self._identifier.value] = self._selected
