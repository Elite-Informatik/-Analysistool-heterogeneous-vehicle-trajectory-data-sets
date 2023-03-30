import unittest

from src.data_transfer.content.error import ErrorMessage
from src.data_transfer.exception import ExecutionFlowError
from src.data_transfer.record import PolygonRecord
from src.data_transfer.record import PositionRecord
from src.model.polygon_structure.polygon import Polygon


class TestPolygon(unittest.TestCase):
    def test_valid_polygon(self):
        """
        Test that a valid polygon can be created.
        :return:
        """
        polygon_record = PolygonRecord((PositionRecord(45, 90),
                                        PositionRecord(45, 0),
                                        PositionRecord(0, 0)),
                                       'valid polygon')
        polygon = Polygon(polygon_record)
        self.assertIsNotNone(polygon.create_polygon_record().name)
        self.assertIsNotNone(polygon.get_id())
        self.assertEqual(len(polygon.get_corners()), 3)

    def polygon_returns_invalid(self, polygon: Polygon) -> ErrorMessage:
        """
        Helper method that checks if an id record of an invalid polygon is correctly setup.
        :param polygon: The polygon to be checked.
        :return: The IDRecord of the polygon for further testing.
        """
        polygon_id = polygon.get_id()
        self.assertRaises(ExecutionFlowError, polygon.create_polygon_record)
        self.assertIsNone(polygon_id)
        return polygon.get_error()

    def test_polygon_with_too_few_points(self):
        """
        Test if a Polygon initialized with to few points returns the correct error.
        """
        polygon_record = PolygonRecord(tuple([PositionRecord(45, 90)]),
                                       'too_few_points')
        polygon = Polygon(polygon_record)
        self.assertEqual(self.polygon_returns_invalid(polygon), ErrorMessage.POLYGON_TOO_FEW_POINTS)

    def test_polygon_with_illegal_coordinates(self):
        """
        Test if a Polygon initialized with incorrect points returns the correct error.
        """
        polygon_record = PolygonRecord((PositionRecord(45, 180),
                                        PositionRecord(45, 0),
                                        PositionRecord(0, 181)),
                                       'illegal_coordinates')
        polygon = Polygon(polygon_record)
        self.assertEqual(self.polygon_returns_invalid(polygon), ErrorMessage.POLYGON_ILLEGAL_COORDINATES)

    def test_polygon_with_invalid_name(self):
        """
        Test if a Polygon initialized with an invalid _name returns the correct error.
        """
        polygon_record = PolygonRecord((PositionRecord(45, 90),
                                        PositionRecord(45, 0),
                                        PositionRecord(0, 0)),
                                       'invalid _name🔥')
        polygon = Polygon(polygon_record)
        self.assertEqual(self.polygon_returns_invalid(polygon), ErrorMessage.INVALID_NAME)


if __name__ == '__main__':
    unittest.main()
