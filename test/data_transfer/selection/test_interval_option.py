import unittest

from src.data_transfer.selection.interval_value_option import IntervalValueOption
from src.data_transfer.selection.option_type import OptionType


class IntervalOptionTest(unittest.TestCase):

    def test_init(self):
        start = 0
        end = 10
        option = IntervalValueOption(start, end)
        self.assertEqual(option._start, start)
        self.assertEqual(option._end, end)
        self.assertEqual(option.get_option_type(), OptionType.INTERVAL_OPTION)

    def test_isValid(self):
        option = IntervalValueOption(5, 10)
        self.assertTrue(option.is_valid(5))
        self.assertTrue(option.is_valid(10))
        self.assertTrue(option.is_valid(7))
        self.assertFalse(option.is_valid(3))
        self.assertFalse(option.is_valid(11))

    def test_getOption(self):
        start = 0
        end = 10
        option = IntervalValueOption(start, end)
        self.assertEqual(option.get_option(), [start, end])

    def test_equal(self):
        option1 = IntervalValueOption(1, 10)
        option2 = IntervalValueOption(1, 10)
        option3 = IntervalValueOption(1, 11)
        self.assertEqual(option1, option2)
        self.assertNotEqual(option1, option3)


if __name__ == '__main__':
    unittest.main()
