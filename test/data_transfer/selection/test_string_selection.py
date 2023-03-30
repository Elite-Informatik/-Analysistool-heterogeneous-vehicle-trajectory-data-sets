import unittest

from src.data_transfer.selection.option_type import OptionType
from src.data_transfer.selection.string_option import StringOption


class StringOptionTest(unittest.TestCase):

    def test_init(self):
        """
        Test that the valid_string attribute and _column attribute are set correctly during initialization
        """
        valid_string = '^[A-Za-z]*$'
        option = StringOption(valid_string)
        self.assertEqual(option._valid_string, valid_string)
        self.assertEqual(option.get_option_type(), OptionType.STRING_OPTION)

    def test_isValid(self):
        """
        Test that the isValid method correctly matches the input string with the regular expression stored in
        valid_string attribute
        """
        option = StringOption('^[A-Za-z]*$')
        self.assertTrue(option.is_valid('abc'))
        self.assertTrue(option.is_valid('ABC'))
        self.assertTrue(option.is_valid('AbC'))
        self.assertFalse(option.is_valid('abc1'))
        self.assertFalse(option.is_valid('abc#'))

    def test_getOption(self):
        """
        Test that the getOption method correctly converts the valid_string attribute to a list of characters
        """
        valid_string = '^[A-Za-z]*$'
        option = StringOption(valid_string)
        self.assertEqual(option.get_option(), list(valid_string))

    def test_equal(self):
        option1 = StringOption("a")
        option2 = StringOption("a")
        option3 = StringOption("a*")
        self.assertEqual(option1, option2)
        self.assertNotEqual(option1, option3)


if __name__ == '__main__':
    unittest.main()
