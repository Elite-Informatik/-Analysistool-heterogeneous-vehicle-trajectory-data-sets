from typing import List

from pandas import DataFrame

from src.data_transfer.content import Column
from src.data_transfer.content import SettingsEnum
from src.data_transfer.record import SelectionRecord
from src.data_transfer.record import SettingsRecord
from src.data_transfer.record import TrajectoryRecord
from src.model.setting_structure.setting_type import Color
from test.controller.test_command import StartedStoppedControllerTest


class FiltererTest(StartedStoppedControllerTest):
    """
    This class tests the filterer.
    """

    def setUp(self) -> None:
        """
        opens the dataset for the tests.
        """
        super().setUp()
        self.open_dataset_intern(path="file/data_for_tests/intern_data_performance_test.csv")

    def test_get_shown_trajectories(self):
        """
        tests the filterer for the get_shown_trajectory method. It checks if the filtered trajectories are the same as
        the raw_data trajectories. It especially checks if the datapoints are in the same order as the raw_data.
        """
        self.maxDiff = None  # show the whole diff
        all_data: DataFrame = self.controller.data_request_facade.get_rawdata(
            selected_column=[Column.TRAJECTORY_ID, Column.LATITUDE, Column.LONGITUDE, Column.TIME]).data
        step_size_setting: List[SelectionRecord] = self.controller.data_request_facade.get_settings() \
            .find(SettingsEnum.TRAJECTORY_STEP_SIZE)
        self.assertIsNotNone(step_size_setting)  # check if the setting exists
        self.assertEqual(len(step_size_setting), 1)  # check if the setting exists only once
        selected: List[int] = step_size_setting[0].selected
        self.assertEqual(len(selected), 1)  # check if the setting is selected only once
        step_size: int = selected[0]
        trajectory_list: List[TrajectoryRecord] = self.controller.data_request_facade.get_shown_trajectories()
        self.assertIsNotNone(trajectory_list)
        self.assertNotEqual(len(trajectory_list), 0)
        for i, trajectory in enumerate(trajectory_list):
            with self.subTest(msg=f"trajectory {i} test", i=i):
                trajectory_id = trajectory.id
                # check that the datapoints in the trajectory are the same as the raw_data
                trajectory_data: DataFrame = self.controller.data_request_facade \
                    .get_rawdata_trajectory(trajectory=trajectory_id).data.sort_values(Column.TIME.value)
                full_longitude_list: List[float] = trajectory_data[Column.LONGITUDE.value].to_list()
                full_latitude_list: List[float] = trajectory_data[Column.LATITUDE.value].to_list()
                actual_longitude_list: List[float] = [point.position.longitude
                                                      for point in trajectory.datapoints]
                actual_latitude_list: List[float] = [point.position.latitude
                                                     for point in trajectory.datapoints]
                expected_longitude_list: List[float] = self.convert_list_to_step_list(full_longitude_list, step_size)
                expected_latitude_list: List[float] = self.convert_list_to_step_list(full_latitude_list, step_size)
                self.assertListEqual(expected_latitude_list, actual_latitude_list)
                self.assertListEqual(expected_longitude_list, actual_longitude_list)

    def convert_list_to_step_list(self, list_to_convert: List[float], step: int) -> List[float]:
        """
        converts a list to a list with the same length but only every step element is in the list.
        The first and the last element are always in the list.
        :param list_to_convert: the list to convert
        :param step: the step size
        """
        result_list: List[float] = []
        if step == 0 or len(list_to_convert) == 0:
            return result_list
        elif len(list_to_convert) == 1 or step == 1:
            return list_to_convert
        result_list.append(list_to_convert[0])
        for i in range(1, len(list_to_convert) - 1, step):
            result_list.append(list_to_convert[i])
        result_list.append(list_to_convert[-1])
        return result_list

    def test_get_parameterized(self):
        """
        tests the filterer for the get_parameterized method. It changes the trajectory color settings to parameter and
        sets the parameter once for each parameter in the number interval column.
        """
        self.maxDiff = None
        all_data = self.controller.data_request_facade.get_rawdata([Column.TRAJECTORY_ID,
                                                                    Column.LATITUDE,
                                                                    Column.LONGITUDE,
                                                                    Column.ACCELERATION,
                                                                    Column.ACCELERATION_DIRECTION])
        settings: SettingsRecord = self.controller.data_request_facade.get_settings()
        color_selection: SelectionRecord = settings.find(SettingsEnum.COLOR_SETTINGS)[0]
        settings = settings.change(SettingsEnum.COLOR_SETTINGS, color_selection.set_selected([Color.PARAMETER]))
        self.controller.communication_facade.change_settings(settings)
        for i, parameter in enumerate(Column.get_number_interval_columns()):
            with self.subTest(msg=f"coloring trajectories with column {parameter.value} test", i=i):
                param_selection: SelectionRecord = settings.find(SettingsEnum.TRAJECTORY_PARAM_COLOR)[0]
                settings = settings.change(SettingsEnum.TRAJECTORY_PARAM_COLOR,
                                           param_selection.set_selected([parameter]))
                self.controller.communication_facade.change_settings(settings)
                data: [TrajectoryRecord] = self.controller.data_request_facade.get_shown_trajectories()
                self.assertIsNotNone(data)
