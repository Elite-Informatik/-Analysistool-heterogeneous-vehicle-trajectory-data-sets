from test.controller.test_command import *
from src.data_transfer.content.settings_enum import SettingsEnum


class TestIntegration1(StartedStoppedControllerTest):
    def test_integrieren(self):
        self.current_dir = os.getcwd()
        os.chdir(os.path.join(os.path.dirname(self.current_dir), 'test'))

        with self.subTest("import dataset"):
            self.controller.communication_facade.import_dataset(["file/example_data_generated/intern_data.csv"],
                                                                "test_data", "intern")
            self.assertEqual(len(self.messages), 1)
            self.messages.pop()
            self.check_event_types([DatasetAdded])
            uuid = self.get_first_event().id

        with self.subTest("open dataset"):
            self.controller.communication_facade.open_dataset(uuid)
            self.check_event_types([DatasetOpened, RefreshTrajectoryData])
            self.get_first_event()
            self.get_first_event()

        with self.subTest("change settings"):
            settings = self.controller.data_request_facade.get_settings()
            selection = settings.find(SettingsEnum.TRAJECTORY_SAMPLE_SIZE)
            self.backup = selection
            selection = selection[0].set_selected([5])
            settings = settings.change(
                identifier=SettingsEnum.TRAJECTORY_SAMPLE_SIZE,
                value=selection
            )
            self.controller.communication_facade.change_settings(settings)
            self.check_event_types([SettingsChanged])
            self.get_first_event()
            self.assertEqual(
                self.controller.data_request_facade.get_settings().find(SettingsEnum.TRAJECTORY_SAMPLE_SIZE)[0].selected[0],
                5
            )

        trajectorys = self.controller.data_request_facade.get_shown_trajectories()

        with self.subTest("Check number of trajectories"):
            self.assertEqual(len(trajectorys), 5, f"5 Trajectories should be shown, but {len(trajectorys)} are shown")

        with self.subTest("Check if all trajectory data is not None"):
            for trajecotry in trajectorys:
                self.assertIsNotNone(trajecotry.id)
                self.assertIsNotNone(trajecotry.datapoints)
                for datapoint in trajecotry.datapoints:
                    self.assertIsNotNone(datapoint)
                    self.assertIsNotNone(datapoint.position)
                    self.assertIsNotNone(datapoint.id)
                    self.assertIsNotNone(datapoint.visualisation)

        with self.subTest("delete dataset"):
            self.controller.communication_facade.delete_dataset(uuid)
            self.check_event_types([DatasetDeleted])
            self.get_first_event()
            self.assertEqual(len(self.messages), 1)
            self.messages.pop()

        with self.subTest("set back settings"):
            settings = settings.change(
                identifier=SettingsEnum.TRAJECTORY_SAMPLE_SIZE,
                value=self.backup
            )
            self.controller.communication_facade.change_settings(settings)
            self.check_event_types([SettingsChanged])
            self.get_first_event()
