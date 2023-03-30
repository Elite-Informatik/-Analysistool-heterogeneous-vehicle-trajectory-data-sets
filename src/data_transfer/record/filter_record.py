from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from src.data_transfer.record.setting_record import SettingRecord


@dataclass(frozen=True)
class FilterRecord:
    """
    record containing all information about a filter
    """

    _name: str
    _structure_name: str
    _enabled: bool
    _negated: bool
    _type: str
    _interval_setting: Optional[SettingRecord]
    _polygon_setting: Optional[SettingRecord]
    _discrete_setting: Optional[SettingRecord]
    _column_setting: Optional[SettingRecord]

    @property
    def name(self) -> str:
        """
        the name
        """
        return self._name

    @property
    def structure_name(self) -> str:
        """
        in which filter structure the filter is in (trajectory or datapoint)
        """
        return self._structure_name

    @property
    def enabled(self) -> bool:
        """
        whether the filter is enabled
        """
        return self._enabled

    @property
    def negated(self) -> bool:
        """
        whether the filter is negated
        """
        return self._negated

    @property
    def type(self) -> str:
        """
        the type of the filter
        """
        return self._type

    @property
    def intervall(self) -> Optional[SettingRecord]:
        """
        the interval selection
        """
        return self._interval_setting

    @property
    def polygons(self) -> Optional[SettingRecord]:
        """
        the polygon selection
        """
        return self._polygon_setting

    @property
    def discrete(self) -> Optional[SettingRecord]:
        """
        the discrete selection
        """
        return self._discrete_setting

    @property
    def column(self) -> Optional[SettingRecord]:
        """
        the column selection
        """
        return self._column_setting

    def enable(self) -> FilterRecord:
        """
        Returns the exact same filter record except that the enabled attribute is set to True
        """
        return FilterRecord(_name=self._name,
                            _structure_name=self._structure_name,
                            _enabled=True,
                            _negated=self._negated,
                            _type=self._type,
                            _interval_setting=self._interval_setting,
                            _polygon_setting=self._polygon_setting,
                            _discrete_setting=self._discrete_setting,
                            _column_setting=self._column_setting)

    def disable(self) -> FilterRecord:
        """
        Returns the exact same filter record except that the disabled attribute is set to False
        """
        return FilterRecord(_name=self._name,
                            _structure_name=self._structure_name,
                            _enabled=False,
                            _negated=self._negated,
                            _type=self._type,
                            _interval_setting=self._interval_setting,
                            _polygon_setting=self._polygon_setting,
                            _discrete_setting=self._discrete_setting,
                            _column_setting=self._column_setting)

    def __eq__(self, other) -> bool:
        if not isinstance(other, FilterRecord):
            return False

        if other.name != self._name or other.structure_name != self._structure_name or other.enabled != self._enabled \
                or other.negated != self._negated or other.type != self._type:
            return False

        if other.discrete != self._discrete_setting or other.polygons != self._polygon_setting \
                or other.intervall != self._interval_setting:
            return False
        return True
