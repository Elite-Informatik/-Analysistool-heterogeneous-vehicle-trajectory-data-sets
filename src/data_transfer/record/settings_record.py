from __future__ import annotations

from dataclasses import dataclass
from typing import List
from typing import Tuple

from src.data_transfer.content.settings_enum import SettingsEnum
from src.data_transfer.record.selection_record import SelectionRecord
from src.data_transfer.record.setting_record import SettingRecord


@dataclass(frozen=True)
class SegmentRecord:
    """
    represents a segment record that contains a  set of setting records
    """
    _settings: Tuple[SettingRecord, ...]
    _name: str
    _identifier: SettingsEnum = SettingsEnum.DEF_SETTING

    @property
    def segment(self):
        """
        returns the name and the set of settings
        :return     name, set of settings
        """
        return self._name, self._settings

    @property
    def name(self):
        """
        the name
        """
        return self._name

    @property
    def setting_records(self) -> Tuple[SettingRecord, ...]:
        """
        the set of settings
        """
        return self._settings

    @property
    def identifier(self):
        """
        the identifier
        """
        return self._identifier

    def change(self, identifier: SettingsEnum, value: SelectionRecord) -> SegmentRecord:
        """
        creates and returns a new segment record with the new selected value
        :param identifier:  the identifier of the selection record to change
        :param value:       the new selected value
        :return             the new segment record
        """
        new_setting = list()
        for setting in self._settings:
            new_setting.append(setting.change(identifier, value))
        return SegmentRecord(tuple(new_setting), self._name, self._identifier)

    def find(self, key: SettingsEnum) -> List[SelectionRecord]:
        """
        returns all selection record whose identifier match the given key
        :param key: the key
        :return     all selection record that match
        """
        values = list()
        for setting in self._settings:
            value = setting.matches(key)
            if value is not None:
                values.append(value)
        return values

    def equal_structure(self, o: SegmentRecord) -> bool:
        """
        Checks if the structure is equal
        """
        if o is None:
            return False
        if not isinstance(o, SegmentRecord):
            return False
        if o._identifier != self._identifier:
            return False
        if o._name != self._name:
            return False

        already_seen: dict = {}
        for setting in self._settings:
            already_seen[id(setting)] = False

        for setting in self._settings:
            for o_setting in o._settings:
                if o_setting.identifier == setting.identifier:
                    if already_seen[id(setting)]:
                        return False
                    already_seen[id(setting)] = True
                    if not setting.equal_structure(o_setting):
                        return False
        return True


@dataclass(frozen=True)
class PageRecord:
    """
    record that contains a set of segment records
    """

    _segments: Tuple[SegmentRecord, ...]
    _name: str
    _identifier: SettingsEnum = SettingsEnum.DEF_SETTING

    @property
    def page_tuple(self):
        """
        returns the name and the set of segments
        """
        return self._name, self._segments

    @property
    def name(self):
        """
        the name
        """
        return self._name

    @property
    def segment_records(self):
        """
        the set of segment records
        """
        return self._segments

    @property
    def identifier(self):
        """
        the identifier
        """
        return self._identifier

    def change(self, identifier: SettingsEnum, value: SelectionRecord) -> PageRecord:
        """
        creates and returns a new page record with the new selected value
        :param identifier   the identifier of the setting record to change
        :param value:       the new selected value
        """
        new_segment = list()
        for segment in self._segments:
            new_segment.append(segment.change(identifier, value))
        return PageRecord(tuple(new_segment), self._name, self._identifier)

    def find(self, key: SettingsEnum) -> [SelectionRecord]:
        """
        gets all contained selection records that match the given key
        :param key:     the key
        :return         all selection records that match
        """
        values = list()
        for segment in self._segments:
            values.extend(segment.find(key))
        return values

    def equal_structure(self, o: PageRecord) -> bool:
        """
        Checks if the structure is equal
        """
        if o is None:
            return False
        if not isinstance(o, PageRecord):
            return False
        if o._identifier != self._identifier:
            return False
        if o._name != self._name:
            return False

        already_seen: dict = {}
        for segment in self._segments:
            already_seen[id(segment)] = False

        for segment in self._segments:
            for o_segment in o._segments:
                if o_segment.identifier == segment.identifier:
                    if already_seen[id(segment)]:
                        return False
                    already_seen[id(segment)] = True
                    if not segment.equal_structure(o_segment):
                        return False
        return True


@dataclass(frozen=True)
class SettingsRecord:
    """
    represents a record holding a set of page records
    (used to represent the settings)
    """

    _pages: Tuple[PageRecord, ...]

    @property
    def pages(self):
        """
        the pages
        """
        return self._pages

    def change(self, identifier: SettingsEnum, value: SelectionRecord):
        """
        creates and returns a new settings record with the new selected value
        :param identifier: the identifier of the selection record to change
        :param value:      the new selected value
        :return            the new settings record
        """
        new_page = list()
        for page in self._pages:
            new_page.append(page.change(identifier, value))
        return SettingsRecord(tuple(new_page))

    def find(self, key: SettingsEnum) -> List[SelectionRecord]:
        """
        gets all contained selection records that match the given key
        :param key:     the key
        :return         all selection records that match
        """
        values = list()
        for page in self._pages:
            values.extend(page.find(key))
        return values

    def equal_structure(self, o: SettingsRecord) -> bool:
        """
        Checks if the structure is equal
        """
        if o is None:
            return False
        if not isinstance(o, SettingsRecord):
            return False

        already_seen: dict = {}
        for page in self._pages:
            already_seen[id(page)] = False

        for page in self._pages:
            for o_page in o._pages:
                if o_page.identifier == page.identifier:
                    if already_seen[id(page)]:
                        return False
                    already_seen[id(page)] = True
                    if not page.equal_structure(o_page):
                        return False
        return True
