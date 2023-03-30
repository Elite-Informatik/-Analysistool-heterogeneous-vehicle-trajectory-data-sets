from dataclasses import dataclass
from typing import Generic
from typing import List
from typing import Optional
from typing import TypeVar
from typing import Union

from src.data_transfer.content.settings_enum import SettingsEnum
from src.data_transfer.record.selection_record import SelectionRecord

T = TypeVar("T")


@dataclass(frozen=True)
class SettingRecord(Generic[T]):
    """
    record containing a selection record representing a setting
    """
    _context: str
    _selection: SelectionRecord[T]
    _identifier: SettingsEnum = SettingsEnum.DEF_SETTING
    _tip: Optional[str] = None

    @classmethod
    def boolean_setting(cls, context: str, identifier: SettingsEnum = SettingsEnum.DEF_SETTING):
        """
        Creates a boolean setting
        """
        selection = SelectionRecord.bool()
        return SettingRecord(context, selection, identifier)

    @classmethod
    def discrete_setting(cls, setting_context: str, options: List[T],
                         identifier: SettingsEnum = SettingsEnum.DEF_SETTING) -> Optional['SettingRecord']:
        """
        creates a new setting record out of the parameters
        """
        if len(options) <= 0:
            return None
        return SettingRecord(setting_context, SelectionRecord.get_list_selection(options), identifier)

    @property
    def current(self):
        """
        the currently selected item
        """
        if len(self._selection.selected) <= 0:
            return None
        return self._selection.selected[0]

    @property
    def context(self):
        """
        the context
        """
        return self._context

    @property
    def selection(self):
        """
        the selection
        """
        return self._selection

    @property
    def identifier(self):
        """
        the identifier
        """
        return self._identifier

    @property
    def tip(self):
        """
        the tip
        """
        return self._tip

    def change(self, identifier: SettingsEnum, value: SelectionRecord):
        """
        creates a new setting record with the given selected value
        :param identifier:  the new identifier
        :param value:       the new selected value
        :return             the new SettingRecord
        """
        if identifier != self._identifier:
            return self
        if not self._selection.check_equal_type(value):
            return self
        new_selection: SelectionRecord = self._selection.set_selected(value.selected)
        return SettingRecord(self._context, new_selection, self._identifier)

    def matches(self, key: SettingsEnum) -> Union[SelectionRecord, None]:
        """
        returns itself if identifier matches the given key
        :param key:     the key
        :return         itself if match
        """
        if self._identifier != key:
            return None
        return self._selection

    def equal_structure(self, o) -> bool:
        """
        Checks if the structure is equal
        """
        if o is None:
            return False
        if not isinstance(o, SettingRecord):
            return False
        if o._identifier != self._identifier:
            return False
        if o._context != self._context:
            return False

        return self.selection.check_equal_type(o._selection)

    def __eq__(self, other):
        if not isinstance(other, SettingRecord):
            return False
        if self._context != other.context or self._identifier != other.identifier:
            return False
        if self._selection != other._selection:
            return False
        return True
