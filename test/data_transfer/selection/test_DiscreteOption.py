import unittest

from src.data_transfer.selection.discrete_option import DiscreteOption
from src.data_transfer.selection.option_type import OptionType


class DiscreteOptionTest(unittest.TestCase):

    def test_something(self):
        options = DiscreteOption([1, 2, 3, 4, ])
        self.assertTrue(options.is_valid(2))
        self.assertFalse(options.is_valid(5))
        self.assertEqual(OptionType.DISCRETE_OPTION, options._optionType)
        options = DiscreteOption([])
        self.assertFalse(options.is_valid(1))

    def test_equal(self):
        option1 = DiscreteOption([1, 10])
        option2 = DiscreteOption([1, 10])
        option3 = DiscreteOption([1, 10, 5])
        self.assertEqual(option1, option2)
        self.assertNotEqual(option1, option3)


if __name__ == '__main__':
    unittest.main()
