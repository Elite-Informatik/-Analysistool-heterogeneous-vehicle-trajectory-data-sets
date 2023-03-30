import uuid
from unittest import TestCase
from unittest.mock import MagicMock

from src.data_transfer.content import Column
from src.data_transfer.content.settings_enum import SettingsEnum
from src.data_transfer.exception.custom_exception import UnexpectedArgumentError
from src.data_transfer.record import PolygonRecord
from src.data_transfer.record import PositionRecord
from src.data_transfer.record.filter_record import FilterRecord
from src.data_transfer.record.id_record import IDRecord
from src.data_transfer.record.selection_record import SelectionRecord
from src.data_transfer.record.setting_record import SettingRecord
from src.data_transfer.selection.discrete_option import DiscreteOption
from src.data_transfer.selection.number_interval_option import NumberIntervalOption
from src.model.filter_structure.composite.filters.interval_filter import IntervalFilter
from src.model.filter_structure.composite.filters.polygon_filter import PolygonFilter
from src.model.polygon_structure.polygon_structure import PolygonStructure


class FilterTest(TestCase):

    def test_filter(self):
        polygon1_uuid = uuid.uuid1()
        polygon1_name = "test_polygon_1"
        polygon_structure = PolygonStructure()
        polygon_structure.get_polygon = MagicMock(return_value=PolygonRecord(tuple(), polygon1_name))
        polygon_structure.get_all_polygons = MagicMock(return_value=[PolygonRecord(tuple(), polygon1_name)])
        polygon_structure.get_all_polygon_ids = MagicMock(return_value=[polygon1_uuid])

        # change
        filter1 = PolygonFilter(uuid.uuid1(), 'filter_record_discrete1', polygon_structure, [])
        filter_change = PolygonFilter(uuid.uuid1(), 'filter1_change', polygon_structure, [polygon1_uuid])
        filter_change_record = filter_change.to_record("struktur")
        filter1.change(filter_change_record)
        self.assertEqual(filter1._polygon_ids, [polygon1_uuid], 'filter should have been changed')

        # get filter
        self.assertEqual(filter1.get_filter(filter1.get_id()), filter1)
        self.assertIsNone(filter1.get_filter(uuid.uuid1()))

        # is polygon in use
        self.assertTrue(filter1.is_polygon_in_use(polygon1_uuid))

    def test_interval_filter(self):
        filter_record_interval1 = FilterRecord(
            _name="filtiyyy",
            _negated=False,
            _enabled=True,
            _structure_name="point filters",
            _type="interval filter",
            _interval_setting=SettingRecord(
                _context="Column for Intervall Filter",
                _selection=SelectionRecord(
                    selected=[Column.SPEED],
                    option=DiscreteOption(
                        options=Column.list()
                    )
                ),
                _identifier=SettingsEnum.COLUMN
            ),
            _column_setting=None,
            _discrete_setting=None,
            _polygon_setting=None
        )

        filter_record_interval2 = FilterRecord(
            _name="filtiyyy",
            _negated=False,
            _enabled=True,
            _structure_name="point filters",
            _type="interval filter",
            _interval_setting=SettingRecord(
                _context="Interval for Interval Filter",
                _selection=SelectionRecord(
                    selected=[[1, 12]],
                    option=NumberIntervalOption(1, 12),
                    possible_selection_range=range(1, 3)
                ),
                _identifier=SettingsEnum.INTERVAL
            ),
            _column_setting=SettingRecord(
                _context="Column for Interval Filter",
                _selection=SelectionRecord(
                    selected=[Column.SPEED],
                    option=DiscreteOption(
                        options=Column.list()
                    )
                ),
                _identifier=SettingsEnum.COLUMN
            ),
            _discrete_setting=None,
            _polygon_setting=None
        )

        interval_filter = IntervalFilter(
            uuid.uuid4(),
            "aaale"
        )
        self.assertTrue(interval_filter.change(filter_record_interval2))
        with self.assertRaises(UnexpectedArgumentError):
            interval_filter.change(filter_record_interval1)
        # self.assertFalse(interval_filter.change(filter_record_interval1))
        self.assertIsNone(interval_filter.get(uuid.uuid4()))
        self.assertFalse(interval_filter.is_polygon_in_use(uuid.uuid1()))

    def test_polygon_filter(self):
        polygon_structure = PolygonStructure()
        uuid_polygon1 = polygon_structure.add_polygon(PolygonRecord(
            (PositionRecord(0, 1), PositionRecord(1, 1), PositionRecord(1, 0), PositionRecord(0, 0))
            , "test_polygon_1")
        )
        filter_record_polygon1 = FilterRecord(
            _name="filtiyyy",
            _negated=False,
            _enabled=True,
            _structure_name="point filters",
            _type="polygon filter",
            _interval_setting=None,
            _column_setting=None,
            _discrete_setting=None,
            _polygon_setting=SettingRecord(
                _context="Polygon for Polygon Filter",
                _selection=SelectionRecord(
                    selected=[IDRecord(uuid_polygon1, "test_polygon_1")],
                    option=DiscreteOption(
                        options=[IDRecord(uuid_polygon1, "test_polygon_1")]
                    )
                ),
                _identifier=SettingsEnum.POLYGON
            )
        )

        filter_record_polygon_invalid = FilterRecord(
            _name="filtiyyy",
            _negated=False,
            _enabled=True,
            _structure_name="point filters",
            _type="polygon filter",
            _interval_setting=None,
            _column_setting=None,
            _discrete_setting=None,
            _polygon_setting=SettingRecord(
                _context="Polygon for Polygon Filter",
                _selection=SelectionRecord(
                    selected=[],
                    option=DiscreteOption(
                        options=[]
                    ),
                    possible_selection_range=range(0, 3)
                ),
                _identifier=SettingsEnum.POLYGON
            )
        )
        polygon_filter = PolygonFilter(
            name="aaaa",
            polygon_structure=polygon_structure,
            polygon_ids=[],
            filter_id=uuid.uuid4()
        )
        self.assertTrue(polygon_filter.change(filter_record_polygon1))
        self.assertFalse(polygon_filter.change(filter_record_polygon_invalid))
