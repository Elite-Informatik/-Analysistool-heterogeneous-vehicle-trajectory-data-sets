import unittest

from src.data_transfer.record.settings_record import SettingsRecord
from src.model.setting_structure.page import Page
from src.model.setting_structure.segment import Segment
from src.model.setting_structure.setting import Setting
from src.model.setting_structure.setting_structure import SettingStructure
from src.data_transfer.content.settings_enum import SettingsEnum

class SettingStructureTest(unittest.TestCase):
    def setUp(self) -> None:
        self.pages = [Page(SettingsEnum.DEF_SETTING, "Page 1",
                           [Segment(SettingsEnum.DEF_SETTING, "Segment 1",
                                    [Setting.from_list("Setting 1", ['A', 'B', 'C'], 'A', SettingsEnum.DEF_SETTING),
                                     Setting.from_interval("Setting 2", 5, 1, 10, SettingsEnum.DEF_SETTING),
                                     Setting.from_string("Setting 3", "[A-Za-z0-9]*", 'abc',
                                                         SettingsEnum.DEF_SETTING)])]),
                      Page(SettingsEnum.DEF_SETTING, "Page 2",
                           [Segment(SettingsEnum.DEF_SETTING, "Segment 3",
                                    [Setting.from_list("Setting 4", ['D', 'E', 'F'], 'D', SettingsEnum.DEF_SETTING)])])]

        self.setting_structure = SettingStructure()
        self.setting_structure._pages = self.pages

    def test_get_settings_record(self):
        settings_record = self.setting_structure.get_settings_record()
        self.assertIsInstance(settings_record, SettingsRecord)

        self.assertEqual(len(settings_record.pages), len(self.pages))

        for i, page_record in enumerate(settings_record.pages):
            page = self.pages[i]
            self.assertEqual(page_record._name, page.get_name())
            self.assertEqual(len(page_record.segment_records), len(page.get_segments()))

            for j, segment_record in enumerate(page_record.segment_records):
                segment = page.get_segments()[j]
                self.assertEqual(segment_record._name, segment.get_name())
                self.assertEqual(len(segment_record.setting_records), len(segment.get_settings()))

                for k, setting_record in enumerate(segment_record.setting_records):
                    setting = segment.get_settings()[k]
                    self.assertEqual(setting_record, setting.get_setting_record())

    def test_update_settings(self):
        structure = SettingStructure()
        settings_record = self.setting_structure.get_settings_record()
        structure.update_settings(settings_record)
        self.assertEqual(structure.get_settings_record(), settings_record)

    def test_update(self):
        structure = SettingStructure()
        settings_record = structure.get_settings_record()
        selection_record = settings_record.find(SettingsEnum.TRAJECTORY_SAMPLE_SIZE)[0].set_selected([4])
        settings_record = settings_record.change(SettingsEnum.TRAJECTORY_SAMPLE_SIZE, selection_record)
        assert (structure.update_settings(settings_record))


if __name__ == '__main__':
    unittest.main()
