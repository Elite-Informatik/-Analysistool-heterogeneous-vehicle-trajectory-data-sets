# this test was created due to a bug in the user tests.
# When reading a first invalid dataset and then a secound valid dataset,
# an error ocurred. This test checks if this error still exists.
import os
from unittest import skip

from src.controller.output_handling.event import DatasetAdded
from src.data_transfer.record import SettingRecord
from test.controller.test_command import StartedStoppedControllerTest


class TestSecoundDatasetFirstInvalidError(StartedStoppedControllerTest):
    def setUp(self) -> None:
        super().setUp()
        import_setting = SettingRecord.boolean_setting(
            "Accept inacurracies?",
            "accept")
        import_setting = import_setting.change("accept", import_setting.selection.set_selected([False]))
        self.returned_selections.append(
            import_setting
        )
        self.current_dir = os.getcwd()
        os.chdir(os.path.join(os.path.dirname(self.current_dir), 'test'))

    def tearDown(self) -> None:
        os.chdir(self.current_dir)
        super().tearDown()

    @skip
    def test_problem(self):
        self.next_answer_to_ask_acceptance.append(False)
        self.controller.communication_facade.import_dataset([
            "file/example_data_generated/01_recordingMeta.csv",
            "file/example_data_generated/01_tracksMeta.csv",
            "file/example_data_generated/42_tracks.csv"
        ],
            "a", "HighD"
        )
        self.assertEqual(1, len(self.errors))
        self.assertEqual(1, len(self.warnings))
        self.warnings.pop()
        self.errors.pop()
        self.open_dataset_highD([
            "file/example_data_generated/01_recordingMeta.csv",
            "file/example_data_generated/01_tracksMeta.csv",
            "file/example_data_generated/01_tracks.csv"
        ])

