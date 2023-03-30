import uuid
from unittest import TestCase
from unittest.mock import MagicMock

from src.data_transfer.content.logical_operator import LogicalOperator
from src.model.filter_structure.composite.filter_group import FilterGroup
from src.model.filter_structure.composite.filters.polygon_filter import PolygonFilter
from src.model.filter_structure.filter_handler import FilterHandler


class FilterStructureTest(TestCase):

    def test_filter_structure(self):
        root_group = FilterGroup(LogicalOperator.AND, uuid.uuid4(), 'standard')
        filter_structure = FilterHandler(root_group, 'lol')

        # Test adding a filters component
        component = PolygonFilter(uuid.uuid4(), 'hi', None, [uuid.uuid1()])
        result = filter_structure.add(component, root_group.get_id())
        self.assertEqual(result, True, f'Failed to add filters component: {result}')
        self.assertEqual(filter_structure.get_filter(component.get_id()), component,
                         'Failed to retrieve added filters component')

        # Test deleting a filters component
        parent_id = filter_structure.delete(component.get_id())
        self.assertEqual(parent_id, root_group.get_id(), f'Incorrect parent id returned: {parent_id}')
        self.assertEqual(filter_structure.get_filter(component.get_id()), None, 'Filter component not deleted')

        # Test getting a filters group
        self.assertEqual(filter_structure.get_filter_group(root_group.get_id()), root_group,
                         'Failed to retrieve root group')

        # Test is_polygon_in_use
        self.assertEqual(filter_structure.is_polygon_in_use(
            uuid.uuid1()), False, 'Filter component should not be using a polygon')
        polygon_id = uuid.uuid1()
        mock_polygon_structure = MagicMock()
        component2 = PolygonFilter(uuid.uuid1(), 'hi', mock_polygon_structure, [polygon_id])
        filter_structure.add(component2, root_group.get_id())
        self.assertEqual(filter_structure.is_polygon_in_use(
            polygon_id), True, 'Filter structure should contain a polygon')
