import uuid
from unittest import TestCase

from src.data_transfer.content.logical_operator import LogicalOperator
from src.data_transfer.exception import InvalidUUID
from src.data_transfer.record import FilterGroupRecord
from src.data_transfer.record import PolygonRecord
from src.data_transfer.record import PositionRecord
from src.model.filter_structure.composite.filter_group import FilterGroup
from src.model.filter_structure.composite.filters.polygon_filter import PolygonFilter
from src.model.filter_structure.filter_structure import FilterStructure
from src.model.polygon_structure.polygon_structure import PolygonStructure


class FilterFacadeTest(TestCase):

    def test_filter_facade(self):
        polygon_facade = PolygonStructure()
        filter_facade = FilterStructure(polygon_facade)
        polygon_facade.set_filter_facade(filter_facade)

        root_id = filter_facade.get_point_filter_root_id()
        polygon1 = polygon_facade.add_polygon(
            PolygonRecord(
                _corners=(PositionRecord(0, 9), PositionRecord(9, 9), PositionRecord(9, 0)),
                _name="poly")
        )

        filter1 = PolygonFilter(
            filter_id=uuid.uuid1(),
            name='hi',
            polygon_structure=polygon_facade,
            polygon_ids=[polygon1]
        ).to_record('point filters')

        filter_group1 = FilterGroup(
            logical_operator=LogicalOperator.AND,
            filter_id=uuid.uuid1(),
            name='group1'
        ).to_record('point filters')

        filter_group2 = FilterGroup(
            logical_operator=LogicalOperator.OR,
            filter_id=uuid.uuid1(),
            name='group2'
        ).to_record('point filters')

        # add filter and filtergroup
        filter_group1_id = filter_facade.add_filter_group(root_id, filter_group1)
        filter_group2_id = filter_facade.add_filter_group(root_id, filter_group2)

        filter1_id = filter_facade.add_filter(filter_group1_id, filter1)

        self.assertEqual(filter_facade.get_filter(filter1_id), filter1, 'filter should be successfully added')
        found_group = filter_facade.get_filter_group(filter_group1_id)
        new_filter_group1 = FilterGroupRecord(filter_group1.name, 'point filters', True, False, (filter1_id,),
                                              LogicalOperator.AND.name)
        self.assertEqual(found_group, new_filter_group1, 'filter group should be successfully added')

        # is polygon in use
        self.assertEqual(filter_facade.is_polygon_in_use(polygon1), True, 'Polygon should be in use')

        # move filter to group
        filter_facade.move_filter_to_group(filter1_id, filter_group2_id)
        parent_id = filter_facade.delete_filter_component(filter1_id)
        self.assertEqual(parent_id, filter_group2_id, 'filter should be in group 2')
        self.assertEqual(filter_facade.delete_filter_component(filter_group1_id), root_id,
                         'group should have been in root')
        self.assertEqual(filter_facade.delete_filter_component(filter_group1_id), None,
                         'group should already been deleted')
        self.assertEqual(filter_facade.delete_filter_component(filter_group2_id), root_id,
                         'group should have been in root')

        # filter structure is empty here

        # change filter
        polygon2 = polygon_facade.add_polygon(
            PolygonRecord((PositionRecord(0, 2), PositionRecord(2, 9), PositionRecord(9, 1)), "poly2"))
        polygon3 = polygon_facade.add_polygon(
            PolygonRecord((PositionRecord(0, 9), PositionRecord(1, 1), PositionRecord(9, 99)), "poly3"))
        filter2 = PolygonFilter(uuid.uuid1(), 'filter', polygon_facade, [polygon2, polygon3]).to_record('point filters')

        filter2_id = filter_facade.add_filter(root_id, filter2)
        self.assertEqual(filter_facade.get_filter(filter2_id), filter2)
        filter2_change = PolygonFilter(uuid.uuid1(), 'filter_change', polygon_facade, [polygon2]).to_record(
            'point filters')

        filter_facade.change_filter(filter2_id, filter2_change)
        self.assertEqual(filter_facade.get_filter(filter2_id), filter2_change, 'filter should have been changed')

        # reconstruct
        filter_facade1 = FilterStructure(polygon_facade)
        group_record1 = FilterGroupRecord('group_1', 'point filters', True, False, (), LogicalOperator.AND.name)
        root2_id = filter_facade1.get_point_filter_root_id()
        group1_id = filter_facade1.add_filter_group(root2_id, group_record1)
        filter1_record = PolygonFilter(uuid.uuid4(), 'transit1', polygon_facade, [polygon2]).to_record('point filters')
        filter1_id = filter_facade1.add_filter(group1_id, filter1_record)
        self.assertEqual(filter_facade1.get_filter_group(group1_id),
                         FilterGroupRecord('group_1', 'point filters', True, False, (filter1_id,),
                                           LogicalOperator.AND.name))
        self.assertEqual(filter_facade1.get_filter(filter1_id), filter1_record)

        filter_facade1.delete_filter_component(group1_id)
        self.assertRaises(InvalidUUID, filter_facade1.get_filter_group, group1_id)
        self.assertRaises(InvalidUUID, filter_facade1.get_filter, filter1_id)

        filter_facade1.reconstruct()
        self.assertEqual(filter_facade1.get_filter_group(group1_id),
                         FilterGroupRecord('group_1', 'point filters', True, False, (filter1_id,),
                                           LogicalOperator.AND.name))
        self.assertEqual(filter_facade1.get_filter(filter1_id), filter1_record)
