import unittest

from src.data_transfer.selection.discrete_option import DiscreteOption
from src.data_transfer.selection.interval_value_option import IntervalValueOption
from src.data_transfer.selection.string_option import StringOption
from src.model.setting_structure.setting import Setting


@unittest.skip
class SettingTest(unittest.TestCase):
    def setUp(self) -> None:
        """
        Initialize test data and create setting instances for testing
        """
        self.test_data_valid = [
            (DiscreteOption(['A', 'B', 'C']), 'A'),
            (IntervalValueOption(1, 10), 5),
            (StringOption("[A-Za-z0-9]*"), 'abc')
        ]
        self.test_data_invalid = [
            (DiscreteOption(['A', 'B', 'C']), 'D'),
            (IntervalValueOption(1, 10), 20),
            (StringOption("[A-Za-z0-9]*"), '!')
        ]
        self.settings = []
        for i, (option, default_selected) in enumerate(self.test_data_valid):
            self.settings.append(Setting(option, default_selected, "test setting"))

    def test_invalid_create(self):
        """
        Test that creating a setting with an invalid default option raises a ValueError
        """
        for i, (option, default_selected) in enumerate(self.test_data_invalid):
            with self.subTest(i=i):
                with self.assertRaises(ValueError):
                    setting = Setting(option, default_selected, "test_setting")

    def test_get_selected(self):
        """
        Test that the selected option is returned correctly
        """
        for i, (option, default_selected) in enumerate(self.test_data_valid):
            with self.subTest(i=i):
                self.assertEqual(self.settings[i].get_selected(), default_selected)

    def test_get_options(self):
        """
        Test that the correct set of option is returned
        """
        for i, (option, default_selected) in enumerate(self.test_data_valid):
            with self.subTest(i=i):
                self.assertEqual(self.settings[i].get_options(), option.get_options())

    def test_set_selected_valid(self):
        """
        Test that a valid option can be set as selected and returns True
        """
        self.assertTrue(self.settings[1].set_selected(3))
        self.assertEqual(self.settings[1].get_selected(), 3)

    def test_set_selected_invalid(self):
        """
        Test that an invalid option cannot be set as selected and returns False
        """
        for i, (option, invalid_option) in enumerate(self.test_data_invalid):
            with self.subTest(i=i):
                prev_value = self.settings[i].get_selected()
                self.assertFalse(self.settings[i].set_selected(invalid_option))
                self.assertEqual(self.settings[i].get_selected(), prev_value)

    def test_get_setting_record(self):
        """
        Test that a SettingRecord instance is returned with the correct values
        """
        for i, (option, default_selected) in enumerate(self.test_data_valid):
            with self.subTest(i=i):
                record = self.settings[i].get_setting_record()
                self.assertEqual(record._context, "test setting")
                self.assertEqual(record._selection.option.get_options(), option.get_options())
                self.assertEqual(record._selection.selected, [default_selected])

    def test_create_with_record(self):
        for i, setting in enumerate(self.settings):
            with self.subTest(i=i):
                setting_from_record = Setting.from_record(setting.get_setting_record())
                self.assertEqual(setting.get_setting_record(), setting_from_record.get_setting_record())


if __name__ == '__main__':
    unittest.main()
