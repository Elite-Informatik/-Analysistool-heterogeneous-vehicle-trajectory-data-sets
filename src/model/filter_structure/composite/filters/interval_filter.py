"""
interval_filter.py contains IntervalFilter class.
"""
from uuid import UUID

from src.data_transfer.content import Column
from src.data_transfer.content.settings_enum import SettingsEnum
from src.data_transfer.record.filter_record import FilterRecord
from src.data_transfer.record.selection_record import SelectionRecord
from src.data_transfer.record.setting_record import SettingRecord
from src.data_transfer.selection import DateIntervalOption
from src.data_transfer.selection import TimeIntervalOption
from src.data_transfer.selection.discrete_option import DiscreteOption
from src.data_transfer.selection.number_interval_option import NumberIntervalOption
from src.model.filter_structure.composite.filters.abstract_filter import Filter
from src.model.filter_structure.filter_visitor import IVisitor


class IntervalFilter(Filter):
    """
    represents an interval filters
    """
    FILTERTYPE = "interval filter"

    APPLYABLE_COLUMNS = Column.get_interval_columns()

    def __init__(self, filter_id: UUID, name: str, column: Column = Column.SPEED, start: float = 0, end: float = 0):
        """
        creates a new interval filters
        :param name:    the _name
        :param start:   the start value of the selected interval
        :param end:     the end value of the selected interval
        """
        super().__init__(filter_id=filter_id, name=name, filter_type=self.FILTERTYPE)
        self._column = column
        self._start = start
        self._end = end
        self._option = NumberIntervalOption()

    def change(self, filter_record: FilterRecord) -> bool:
        """
        overwrites its attributes with the given parameters
        :param filter_record:   the parameters
        """
        if not super().change(filter_record) or not self.check_and_set_column(filter_record):
            return False

        if not isinstance(filter_record.intervall, SettingRecord):
            return False

        if not isinstance(filter_record.intervall.selection, SelectionRecord):
            return False

        if filter_record.polygons is not None or filter_record.discrete is not None:
            return False

        if not isinstance(filter_record.intervall.selection.option, NumberIntervalOption) \
                and not isinstance(filter_record.intervall.selection.option, DateIntervalOption) \
                and not isinstance(filter_record.intervall.selection.option, TimeIntervalOption):
            return False

        self._column = filter_record.column.selection.selected[0]
        self._option = filter_record.intervall.selection.option
        self._start = filter_record.intervall.selection.selected[0][0]
        self._end = filter_record.intervall.selection.selected[0][1]
        return True

    def to_record(self, structure_name: str) -> FilterRecord:
        """
        Converts the filter to a record
        :param structure_name: the _name of the structure the filter is in
        :return: a filterrecord of the filter
        """

        interval_selection = SelectionRecord(
            selected=[[self._start, self._end]],
            option=self._option,
            possible_selection_range=range(1, 2)
        )

        interval_setting = SettingRecord(
            _context="Select Interval for Interval Filter",
            _selection=interval_selection,
            _identifier=SettingsEnum.INTERVAL
        )

        column_selection = SelectionRecord(
            selected=[self._column],
            option=DiscreteOption(self.APPLYABLE_COLUMNS),
            possible_selection_range=range(1, 2)
        )

        column_setting = SettingRecord(
            _context="Select Column for Interval Filter",
            _selection=column_selection,
            _identifier=SettingsEnum.COLUMN
        )

        return FilterRecord(
            _name=self._name,
            _structure_name=structure_name,
            _type=self.FILTERTYPE,
            _enabled=self._enabled,
            _negated=self._negated,
            _interval_setting=interval_setting,
            _column_setting=column_setting,
            _discrete_setting=None,
            _polygon_setting=None
        )

    def _accept_visitor(self, v: IVisitor) -> None:
        """
        accepts a visitor
        :param v: the visitor
        """
        v.visit_interval_filter(self)

    @property
    def needs_polygons(self) -> bool:
        """
        return if polygon_structure is needed for filter
        :return: if polygon_structure is needed
        """
        return False

    @property
    def column(self) -> Column:
        """
        gets the selected data
        :return: the selected data
        """
        return self._column

    @property
    def start(self):
        """
        gets the start of the interval
        :return: start of the interval
        """
        return self._option.sql_format().format(data=self._start)

    @property
    def end(self):
        """
        gets the end of the interval
        :return: end of the interval
        """
        return self._option.sql_format().format(data=self._end)
