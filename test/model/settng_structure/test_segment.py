import unittest

from src.data_transfer.content.settings_enum import SettingsEnum
from src.data_transfer.record.settings_record import SegmentRecord
from src.data_transfer.selection.discrete_option import DiscreteOption
from src.model.setting_structure.segment import Segment
from src.model.setting_structure.setting import Setting


class SegmentTest(unittest.TestCase):
    def setUp(self) -> None:
        self.setting_1 = Setting.from_list("Setting 1", ['A', 'B', 'C'], 'A', SettingsEnum.SETTING1)
        self.setting_2 = Setting.from_interval("Setting 2", 5, 1, 10, SettingsEnum.SETTING2)
        self.setting_3 = Setting.from_string("Setting 3", "[A-Za-z0-9]*", 'abc', SettingsEnum.SETTING3)
        self.segment = Segment(SettingsEnum.SEGMENT1, "Test Segment", [self.setting_1, self.setting_2])

    def test_add_setting(self):
        """
        Test that a setting can be added to the segment and the count of settings increases by 1
        """
        initial_count = len(self.segment.get_settings())
        self.assertTrue(self.segment.add_setting(self.setting_3))
        self.assertIn(self.setting_3, self.segment.get_settings())
        self.assertEqual(len(self.segment.get_settings()), initial_count + 1)

    def test_add_setting_duplicate(self):
        """
        Test that a duplicate setting cannot be added to the segment and returns False
        """
        initial_count = len(self.segment.get_settings())
        self.assertFalse(self.segment.add_setting(self.setting_1))
        self.assertEqual(len(self.segment.get_settings()), initial_count)

    def test_get_settings(self):
        """
        Test that the correct settings are returned
        """
        settings = self.segment.get_settings()
        self.assertEqual(settings, [self.setting_1, self.setting_2])

    def test_get_name(self):
        """
        Test that the _name of the segment is returned correctly
        """
        self.assertEqual(self.segment.get_name(), "Test Segment")

    def test_get_record(self):
        '''
        Test that the Segment class returns a correct SegmentRecord object.
        It should contain the same _name as the Segment instance as well as a tuple of SettingRecord objects.
        Those should also match the Setting instances
        :return:
        '''
        # Create a discrete option for the setting
        options = DiscreteOption(["Option 1", "Option 2", "Option 3"])
        default_selected = "Option 2"
        setting = Setting.from_list("Setting 1", ["Option 1", "Option 2", "Option 3"], default_selected,
                                    SettingsEnum.SETTING1)
        # Create a segment with the setting
        segment = Segment(SettingsEnum.SEGMENT1, "Segment 1", [setting])
        # Get the record of the segment
        segment_record = segment.get_record()
        # Assert that the record is of the correct type
        self.assertIsInstance(segment_record, SegmentRecord)
        # Assert that the segment _name and setting list match the original segment
        self.assertEqual(segment_record.segment[0], segment.get_name())
        self.assertEqual(segment_record.segment[1][0].context, setting.get_setting_record().context)
        self.assertEqual(segment_record.segment[1][0].selection.option.get_option_type(), options.get_option_type())
        self.assertEqual(segment_record.segment[1][0].selection.option.get_option(), options.get_option())
        self.assertEqual(segment_record.segment[1][0].selection.selected, [default_selected])


if __name__ == '__main__':
    unittest.main()
