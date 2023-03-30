"""
abstract_filter.py contains Filter class.
"""
from abc import ABC
from abc import abstractmethod
from typing import List
from typing import Optional
from uuid import UUID

from src.model.filter_structure.filter_visitor import IVisitor
from src.data_transfer.content.settings_enum import SettingsEnum
from src.data_transfer.record.filter_record import FilterRecord
from src.data_transfer.record.selection_record import SelectionRecord
from src.data_transfer.record.setting_record import SettingRecord
from src.model.filter_structure.composite.filter_component import FilterComponent
from src.model.polygon_structure.ipolygon_structure import IPolygonStructure
from src.data_transfer.exception.custom_exception import UnexpectedArgumentError, ExceptionMessages


class Filter(FilterComponent, ABC):
    """
    Abstract Filter class for 
    """
    APPLYABLE_COLUMNS = None

    def __init__(self, name: str, filter_id: UUID, filter_type: str = None):
        super().__init__(name=name, filter_id=filter_id)
        self._filter_type = filter_type

    def change(self, filter_record: FilterRecord) -> bool:
        """
        overwrites its attributes with the given parameters
        :param filter_record:   the parameters
        """
        if filter_record.type != self._filter_type:
            raise UnexpectedArgumentError(ExceptionMessages.UNEXPECTED_VALUE.value.format(
                passed_value=filter_record.type, expected_value=self._filter_type,
                additional_info="The type in the filter record is not the same as the type of the filter!"
            ))

        if not isinstance(filter_record.name, str):
            raise UnexpectedArgumentError(ExceptionMessages.UNEXPECTED_TYPE.value.format(
                passed_type=type(filter_record.name), expected_type=str,
                additional_info="The name of the filter record is not a str!"
            ))
        if not isinstance(filter_record.enabled, bool):
            raise UnexpectedArgumentError(ExceptionMessages.UNEXPECTED_TYPE.value.format(
                passed_type=type(filter_record.enabled), expected_type=bool,
                additional_info="The enabled attribute of the filter record is not a bool!"
            ))
        if not isinstance(filter_record.negated, bool):
            raise UnexpectedArgumentError(ExceptionMessages.UNEXPECTED_TYPE.value.format(
                passed_type=type(filter_record.negated), expected_type=bool,
                additional_info="The negated attribute of the filter record is not a bool!"
            ))

        self._name: str = filter_record.name
        self._enabled: bool = filter_record.enabled
        self._negated: bool = filter_record.negated
        self._filter_type: str = filter_record.type
        return True

    def check_and_set_column(self, filter_record: FilterRecord) -> bool:
        """
        checks if the column is correct
        :param filter_record:   the parameters
        """
        if not isinstance(filter_record.column, SettingRecord):
            raise UnexpectedArgumentError(ExceptionMessages.UNEXPECTED_TYPE.value.format(
                passed_type=type(filter_record.column), expected_type=SettingRecord,
                additional_info="The column of the filter record is not a SettingRecord!"
            ))
        if not isinstance(filter_record.column.identifier, SettingsEnum):
            raise UnexpectedArgumentError(ExceptionMessages.UNEXPECTED_TYPE.value.format(
                passed_type=type(filter_record.column.identifier), expected_type=SettingsEnum,
                additional_info="The identifier of the column of the filter record is not a SettingsEnum!"
            ))
        if not isinstance(filter_record.column.context, str):
            raise UnexpectedArgumentError(ExceptionMessages.UNEXPECTED_TYPE.value.format(
                passed_type=type(filter_record.column.context), expected_type=str,
                additional_info="The context of the column setting of the filter record is not a str!"
            ))

        if not isinstance(filter_record.column.selection, SelectionRecord):
            raise UnexpectedArgumentError(ExceptionMessages.UNEXPECTED_TYPE.value.format(
                passed_type=type(filter_record.column.selection), expected_type=SelectionRecord,
                additional_info="The selection of the column setting of the filter record is not a SelectionRecord!"
            ))
        if filter_record.column.identifier != SettingsEnum.COLUMN:
            raise UnexpectedArgumentError(ExceptionMessages.UNEXPECTED_VALUE.value.format(
                passed_value=filter_record.column.identifier, expected_value=SettingsEnum.COLUMN,
                additional_info="The identifier of the column setting of the filter record is not SettingsEnum.COLUMN!"
            ))
        if filter_record.column.selection.selected[0] not in self.APPLYABLE_COLUMNS:
            raise UnexpectedArgumentError(ExceptionMessages.UNEXPECTED_VALUE.value.format(
                passed_value=filter_record.column.selection.selected[0], expected_value=self.APPLYABLE_COLUMNS,
                additional_info="The column of the filter record is not in the applicable columns of the filter!"
            ))
        self._column = filter_record.column.selection.selected[0]
        return True

    @abstractmethod
    def to_record(self, structure_name: str) -> FilterRecord:
        """
        Converts the filter to a record
        :param structure_name: the _name of the structure the filter is in
        :return: a filterrecord of the filter
        """
        pass

    @property
    def needs_polygons(self) -> bool:
        """
        return if polygon_structure is needed for filter
        :return: if polygon_structure is needed
        """
        raise NotImplemented("Function is not implemented for this Filter!")

    def set_polygon_structure(self, polygon_structure: IPolygonStructure) -> None:
        """
        Setter for the polygon_structure of the Filter
        :param polygon_structure: polygon_structure of the Filter
        """
        raise NotImplemented("Function is not implemented for this Filter!")

    def set_polygons(self, polygon_ids: List[UUID]) -> None:
        """
        Setter of the polygons of the filter
        :param polygon_ids: polygons of the filter
        """
        raise NotImplemented("Function is not implemented for this Filter!")

    def get_filter(self, filter_id: UUID) -> Optional['Filter']:
        """
        returns itself if the given id matches the own id
        :param filter_id:  the id
        :return:    itself when id matches the own
        """
        if self._id == filter_id:
            return self
        return None

    def change_enabled(self, enabled: bool, filters: List[UUID], filter_groups: List[UUID]):
        """
        changes the enabled state of the filter
        :param enabled:     the new enabled state
        :param filter_groups:   the filter groups to change
        :param filters:     the filters to change
        """
        if self._enabled == enabled:
            return
        super().change_enabled(enabled, filters, filter_groups)
        filters.append(self._id)

    def accept_visitor(self, v: 'IVisitor') -> None:
        """
        accepts the visitor
        :param v:   the visitor
        """
        if self._enabled:
            self._accept_visitor(v)

    def _accept_visitor(self, v: 'IVisitor') -> None:
        """
        accepts the visitor
        :param v:   the visitor
        """
        raise NotImplemented("Function is not implemented for this Filter!")
