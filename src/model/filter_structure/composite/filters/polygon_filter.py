"""
polygon_filter.py contains PolygonFilter class.
"""

from typing import List
from uuid import UUID

from src.data_transfer.content.settings_enum import SettingsEnum
from src.data_transfer.record.filter_record import FilterRecord
from src.data_transfer.record.id_record import IDRecord
from src.data_transfer.record.polygon_record import PolygonRecord
from src.data_transfer.record.selection_record import SelectionRecord
from src.data_transfer.record.setting_record import SettingRecord
from src.data_transfer.selection.discrete_option import DiscreteOption
from src.model.filter_structure.composite.filters.abstract_filter import Filter
from src.model.filter_structure.filter_visitor import IVisitor
from src.model.polygon_structure.ipolygon_structure import IPolygonStructure


class PolygonFilter(Filter):
    """
    represents a transit filters
    """
    FILTERTYPE = "polygon filter"

    def __init__(self, filter_id: UUID, name: str, polygon_structure: IPolygonStructure = None,
                 polygon_ids: List[UUID] = None):
        """
        creates a new transit filters
        :param filter_id: the id
        :param name: the name
        :param polygon_ids: the polygons through which the trajectories must pass
        """
        super().__init__(filter_id=filter_id, name=name, filter_type=self.FILTERTYPE)
        self._polygon_ids = polygon_ids
        self._polygon_structure = polygon_structure

    @property
    def needs_polygons(self) -> bool:
        """
        return if polygon_structure is needed for filter
        :return: if polygon_structure is needed
        """
        return True

    def set_polygon_structure(self, polygon_structure: IPolygonStructure) -> None:
        """
        Setter for the polygon_structure of the Filter
        :param polygon_structure: polygon_structure of the Filter
        """
        self._polygon_structure = polygon_structure

    def set_polygons(self, polygon_ids: List[UUID]) -> None:
        """
        Setter of the polygons of the filter
        :param polygon_ids: polygons of the filter
        """
        self._polygon_ids = polygon_ids

    def change(self, filter_record: FilterRecord) -> bool:
        """
        overwrites its attributes with the given parameters
        :param filter_record: the parameters
        """
        if not super().change(filter_record):
            return False

        if not isinstance(filter_record.polygons, SettingRecord):
            return False

        if not isinstance(filter_record.polygons.selection, SelectionRecord):
            return False

        if filter_record.discrete is not None or filter_record.intervall is not None \
                or filter_record.column is not None:
            return False

        for polygon_record in filter_record.polygons.selection.selected:
            if not isinstance(polygon_record, IDRecord):
                return False
            if not isinstance(polygon_record.id, UUID):
                return False

        self._polygon_ids = [id_record.id for id_record in filter_record.polygons.selection.selected]
        if len(self._polygon_ids) == 0:
            return False

        return True

    def to_record(self, structure_name: str) -> FilterRecord:
        """
        converts itself to a record
        :return: the filters record of itself
        """

        # get all polygons
        all_polygon_ids = self._polygon_structure.get_all_polygon_ids()
        polygons = list()
        for polygon_id in all_polygon_ids:
            polygon = self._polygon_structure.get_polygon(polygon_id)
            polygons.append(
                IDRecord(
                    polygon_id,
                    polygon.name
                )
            )

        # get selected polygons
        self_polygons = list()
        for polygon_id in self._polygon_ids:
            polygon = self._polygon_structure.get_polygon(polygon_id)
            self_polygons.append(
                IDRecord(
                    polygon_id,
                    polygon.name
                )
            )

        options = DiscreteOption(polygons)

        polygon_selection = SelectionRecord(
            selected=self_polygons,
            option=options,
            possible_selection_range=range(0, len(polygons) + 1)
        )

        polygon_setting = SettingRecord(
            _context="Polygons for Polygon Filter",
            _selection=polygon_selection,
            _identifier=SettingsEnum.POLYGON
        )

        return FilterRecord(
            _name=self._name,
            _structure_name=structure_name,
            _type=self.FILTERTYPE,
            _enabled=self._enabled,
            _negated=self._negated,
            _polygon_setting=polygon_setting,
            _interval_setting=None,
            _column_setting=None,
            _discrete_setting=None

        )

    def _accept_visitor(self, v: IVisitor) -> None:
        """
        accepts a visitor
        :param v: the visitor
        """
        v.visit_polygon_filter(self)

    def is_polygon_in_use(self, polygon_id: UUID) -> bool:
        """
        checks whether the polygon of the given id is used in this filters
        :param polygon_id: the id of the polygon
        :return: whether the id is used
        """
        return polygon_id in self._polygon_ids

    @property
    def polygons(self) -> List[PolygonRecord]:
        """
        gets all polygons of this filters
        :return: all polygons of the filters
        """
        polygons = []
        for polygon_id in self._polygon_ids:
            polygon_record = self._polygon_structure.get_polygon(polygon_id)
            polygons.append(polygon_record)
        return polygons
