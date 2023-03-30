"""
discrete_filter.py contains DiscreteFilter class.
"""
from typing import List
from uuid import UUID

from src.data_transfer.content import Column
from src.data_transfer.content.settings_enum import SettingsEnum
from src.data_transfer.exception.custom_exception import UnexpectedArgumentError, ExceptionMessages
from src.data_transfer.record.filter_record import FilterRecord
from src.data_transfer.record.selection_record import SelectionRecord
from src.data_transfer.record.setting_record import SettingRecord
from src.data_transfer.selection.discrete_option import DiscreteOption
from src.model.filter_structure.composite.filters.abstract_filter import Filter
from src.model.filter_structure.filter_visitor import IVisitor


class DiscreteFilter(Filter):
    """
    represents a discrete filter
    """

    FILTERTYPE = "discrete filter"

    APPLYABLE_COLUMNS = Column.get_discrete_columns()

    def __init__(self, filter_id: UUID, name: str, column: Column = Column.ROAD_TYPE, selection: List[str] = None):
        """
        creates a new discrete filter
        :param filter_id:          the id
        :param name:        the _name
        """
        super().__init__(filter_id=filter_id, name=name, filter_type=self.FILTERTYPE)
        if selection is None:
            selection = list()
        self._column = column
        self._selection = selection
        self._possibel_selection_length = 2

    def change(self, filter_record: FilterRecord) -> bool:
        """
        overwrites its attributes with the given parameters
        :param filter_record: the parameters
        """

        if not super().change(filter_record) or not self.check_and_set_column(filter_record):
            return False

        if not isinstance(filter_record.discrete, SettingRecord):
            raise UnexpectedArgumentError(ExceptionMessages.UNEXPECTED_TYPE.value.format(
                passed_type=type(filter_record.discrete), expected_type=SettingRecord,
                additional_info="The discrete attribute of the filter record is not a SettingRecord!"
            ))

        if not isinstance(filter_record.discrete.selection, SelectionRecord):
            raise UnexpectedArgumentError(ExceptionMessages.UNEXPECTED_TYPE.value.format(
                passed_type=type(filter_record.discrete.selection), expected_type=SelectionRecord,
                additional_info="The selection attribute of the discrete setting record is not a SelectionRecord!"
            ))

        if filter_record.polygons is not None:
            raise UnexpectedArgumentError(ExceptionMessages.UNEXPECTED_TYPE.value.format(
                passed_type=type(filter_record.polygons), expected_type=None,
                additional_info="The polygons attribute of the filter record should be None for the discrete Filter!"
            ))

        if filter_record.intervall is not None:
            raise UnexpectedArgumentError(ExceptionMessages.UNEXPECTED_TYPE.value.format(
                passed_type=type(filter_record.intervall), expected_type=None,
                additional_info="The interval attribute of the filter record should be None for the discrete Filter!"
            ))

        self._possibel_selection_length = filter_record.discrete.selection.possible_selection_amount.stop
        self._selection = filter_record.discrete.selection.selected
        return True

    def to_record(self, structure_name: str) -> FilterRecord:
        """
        converts itself to a record
        :return:    the filters record of itself
        """

        discrete_selection = SelectionRecord(
            selected=self._selection,
            option=DiscreteOption(self._selection),
            possible_selection_range=range(0, self._possibel_selection_length)
        )

        discrete_setting = SettingRecord(
            _context="Select Values for Discrete Filter",
            _selection=discrete_selection,
            _identifier=SettingsEnum.DISCRETE
        )

        column_selection = SelectionRecord(
            selected=[self._column],
            option=DiscreteOption(
                options=self.APPLYABLE_COLUMNS
            ),
            possible_selection_range=range(1, 2)
        )

        column_setting = SettingRecord(
            _context="Select Column for Discrete Filter",
            _selection=column_selection,
            _identifier=SettingsEnum.COLUMN
        )

        return FilterRecord(
            _name=self._name,
            _structure_name=structure_name,
            _enabled=self._enabled,
            _negated=self._negated,
            _type=self.FILTERTYPE,
            _discrete_setting=discrete_setting,
            _column_setting=column_setting,
            _interval_setting=None,
            _polygon_setting=None
        )

    def _accept_visitor(self, v: IVisitor) -> None:
        """
        accepts a visitor
        :param v: the visitor
        """
        v.visit_discrete_filter(self)

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
    def selection(self) -> List[str]:
        """
        gets the discrete selection
        :return: the discrete selection
        """
        return self._selection
