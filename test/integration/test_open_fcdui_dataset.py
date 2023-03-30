import os

from src.data_transfer.content import SettingsEnum
from src.data_transfer.record.setting_record import SettingRecord
from test.controller.test_command import StartedStoppedControllerTest


class OpenFCDUIDatasetControllerTest(StartedStoppedControllerTest):
    def setUp(self) -> None:
        # self.name = HeatmapAnalysis()._name
        super().setUp()
        import_setting = SettingRecord.boolean_setting(
            context="Accept inacurracies?",
            identifier=SettingsEnum.DISCRETE)
        import_setting = import_setting.change("accept", import_setting.selection.set_selected([True]))
        self.returned_selections.append(
            import_setting
        )
        self.current_dir = os.getcwd()
        os.chdir(os.path.join(os.path.dirname(self.current_dir), 'test'))
        self.open_dataset_fcd_ui("file/data_for_tests/part-trimmed.csv")
        # self.controller.communication_facade.open_dataset(self.dataset_uuid)

    def test(self):
        pass
