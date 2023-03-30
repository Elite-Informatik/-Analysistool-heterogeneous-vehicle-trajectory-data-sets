from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class FilterGroupRecord:
    """
    record containing all information about a filter group
    """

    _name: str
    _structure_name: str
    _enabled: bool
    _negated: bool
    _filter_records: tuple  # Tuple[UUID]
    _operator: str

    @property
    def name(self):
        """
        the name
        """
        return self._name

    @property
    def structure_name(self):
        """
        in which filter structure the filter group is in (trajectory or datapoint)
        """
        return self._structure_name

    @property
    def enabled(self):
        """
        whether filter group is enabled
        """
        return self._enabled

    @property
    def negated(self):
        """
        whether filter group is negated
        """
        return self._negated

    @property
    def filter_records(self):
        """
        all contained filters
        """
        return self._filter_records

    @property
    def operator(self):
        """
        the logical operator
        """
        return self._operator

    def enable(self) -> FilterGroupRecord:
        """
        Returns the exact same filter group, except that the enabled attribute is set to True
        """
        return FilterGroupRecord(_name=self._name,
                                 _structure_name=self._structure_name,
                                 _enabled=True,
                                 _negated=self._negated,
                                 _filter_records=self._filter_records,
                                 _operator=self._operator)

    def disable(self) -> FilterGroupRecord:
        """
        Returns the exact same filter group, except that the enabled attribute is set to False
        """
        return FilterGroupRecord(_name=self._name,
                                 _structure_name=self._structure_name,
                                 _enabled=False,
                                 _negated=self._negated,
                                 _filter_records=self._filter_records,
                                 _operator=self._operator)

    def __repr__(self):
        if self._negated:
            return f"not {self._operator} {self._name}"
        else:
            return f"{self._operator} {self._name}"
