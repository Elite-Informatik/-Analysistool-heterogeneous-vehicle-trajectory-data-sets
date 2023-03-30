import unittest

from src.data_transfer.record.position_record import PositionRecord


class PositionRecordTest(unittest.TestCase):
    def test_record(self):
        # list of test cases, each test case is a tuple of (la, lo, expected)
        test_data = [
            (2, 10, {"_latitude": 2, "_longitude": 10}),
            (3, 20, {"_latitude": 3, "_longitude": 20}),
            (4, -10, {"_latitude": 4, "_longitude": -10}),
            (5, 0, {"_latitude": 5, "_longitude": 0}),
            (-2, -10, {"_latitude": -2, "_longitude": -10}),
        ]
        # iterate over test cases
        for i, (la, lo, expected) in enumerate(test_data):
            # create a new subTest for every test case
            with self.subTest(i=i):
                # create a new instance of the PositionRecord class with the input arguments
                record = PositionRecord(_latitude=la, _longitude=lo)
                # assert that the latitude and longitude attributes of the record match the expected values
                self.assertEqual(record.latitude, expected['_latitude'])
                self.assertEqual(record.longitude, expected['_longitude'])


if __name__ == '__main__':
    unittest.main()
