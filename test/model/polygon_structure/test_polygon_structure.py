import uuid as uuid
from unittest import TestCase
from unittest.mock import MagicMock
from uuid import UUID

from src.data_transfer.exception import InvalidUUID
from src.data_transfer.exception import ObjectInUse
from src.data_transfer.record import PolygonRecord
from src.data_transfer.record import PositionRecord
from src.model.polygon_structure.polygon_structure import PolygonStructure


class FilterStructureTest(TestCase):

    # Test Nr.1
    # Checks if polygon is added correctly with record
    # Checks if uuid return is none if not existant
    # Checks if polygon is removable if used in the filter
    def test_polygon_structure(self):
        polygon_structure = PolygonStructure()

        filter_facade = MagicMock()
        filter_facade.is_polygon_in_use = MagicMock(return_value=False)

        polygon_structure.set_filter_facade(filter_facade)

        # create first polygon
        position_0 = PositionRecord(0, 0)
        position_1 = PositionRecord(1, 1)
        position_3 = PositionRecord(0.5, 1.5)
        position_list_0 = [position_0, position_1]

        name: str = "test_polygon_0"
        polygon_uuid: UUID = uuid.uuid4()
        polygon_0 = PolygonRecord(tuple(position_list_0), name)
        returned_id = polygon_structure.add_polygon(polygon_0)
        # print(returned_record)
        self.assertIsNone(returned_id)
        position_list_0.append(position_3)
        polygon_0 = PolygonRecord(tuple(position_list_0), name)
        polygon_structure.add_polygon(polygon_0)

        uuid_list_0 = polygon_structure.get_all_polygon_ids()
        polygon_return_0 = polygon_structure.get_polygon(uuid_list_0[0])

        self.assertEqual(polygon_return_0, polygon_0)

        random_uuid = uuid.uuid4()
        try:
            if polygon_structure.get_polygon(random_uuid):
                self.fail("No exception")
        except InvalidUUID:
            pass

        filter_facade.is_polygon_in_use = MagicMock(return_value=True)
        try:
            if polygon_structure.delete_polygon(uuid_list_0[0]):
                self.fail("Non exception")
        except ObjectInUse:
            pass
