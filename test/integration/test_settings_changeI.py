from src.data_transfer.content.settings_enum import SettingsEnum
from test.integration.test_open_fcdui_dataset import OpenFCDUIDatasetControllerTest


class SettingTest(OpenFCDUIDatasetControllerTest):

    def test_change_setting(self):
        settings = (self.controller.data_request_facade.get_settings())
        new_setting = settings.find(SettingsEnum.TRAJECTORY_SAMPLE_SIZE)[0].set_selected([30])
        settings = settings.change(
            SettingsEnum.TRAJECTORY_SAMPLE_SIZE,
            new_setting
        )
        self.controller.communication_facade.change_settings(settings)
        self.assertEqual(self.controller.data_request_facade.get_settings(), settings)
