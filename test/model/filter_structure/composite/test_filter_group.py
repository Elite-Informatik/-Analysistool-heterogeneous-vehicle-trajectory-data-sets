import uuid
from unittest import TestCase
from unittest.mock import MagicMock

from src.data_transfer.content.logical_operator import LogicalOperator
from src.data_transfer.record import FilterGroupRecord
from src.model.filter_structure.composite.filter_group import FilterGroup
from src.model.filter_structure.composite.filters.polygon_filter import PolygonFilter


class FilterGroupTest(TestCase):

    def test_filter_group(self):
        filter_group = FilterGroup(LogicalOperator.AND, uuid.uuid1(), 'group1')
        filter1 = MagicMock(PolygonFilter)
        filter1_id = uuid.uuid1()
        filter1.get_id = MagicMock(return_value=filter1_id)
        self.assertEqual(filter1.get_id(), filter1_id)
        filter1.get_filter = MagicMock(return_value=filter1)
        filter1.delete = MagicMock(return_value=None)
        filter2 = MagicMock()
        filter2_id = uuid.uuid1()
        filter2.get_filter = MagicMock(return_value=None)
        filter2.get_id = MagicMock(return_value=filter2_id)
        filter2.delete = MagicMock(return_value=None)

        # add
        filter_group.add(filter1, filter_group.get_id())
        self.assertEqual(filter_group.get_filter(filter1_id), filter1)
        # self.assertEqual(filter_group.get_filter(filter2_id), None)

        # to record
        group_record = filter_group.to_record('aal')
        optimal_record = FilterGroupRecord(_name='group1', _structure_name='aal', _enabled=True, _negated=False,
                                           _filter_records=(filter1_id,),
                                           _operator=LogicalOperator.AND.name)
        self.assertEqual(group_record, optimal_record)
        # delete
        self.assertEqual(filter_group.delete(filter2_id), None)
        self.assertEqual(filter_group.delete(filter1_id), filter_group.get_id())

        self.assertEqual(filter_group.get_filter(filter1_id), None)

        # is polygon in use
        filter_group2 = FilterGroup(LogicalOperator.AND, uuid.uuid1(), 'group2')
        polygon1 = uuid.uuid1()
        polygon_filter = PolygonFilter(uuid.uuid1(), 'filter', None, [polygon1])
        self.assertEqual(filter_group2.is_polygon_in_use(polygon1), False)
        filter_group2.add(polygon_filter, filter_group2.get_id())
        self.assertEqual(filter_group2.is_polygon_in_use(polygon1), True)

        # change
        filter_group = FilterGroup(LogicalOperator.AND, uuid.uuid1(), 'hi')
        filter_group_change = FilterGroupRecord('hi_change', 'arr', True, False, (), LogicalOperator.OR.name)
        filter_group.change(filter_group_change, list(), list())
        self.assertEqual(filter_group._logical_operator, LogicalOperator.OR)
