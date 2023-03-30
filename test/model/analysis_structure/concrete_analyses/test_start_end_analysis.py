import time
import unittest
from typing import List
from typing import Tuple
from unittest.mock import Mock
from uuid import uuid4

import pandas as pd

from src.data_transfer.content import Column
from src.data_transfer.record import AnalysisRecord
from src.data_transfer.record import DataPointRecord as DataPoint
from src.data_transfer.record import PolygonRecord
from src.data_transfer.record import PositionRecord as Point
from src.data_transfer.record import TrajectoryRecord
from src.data_transfer.record.selection_record import SelectionRecord
from src.data_transfer.record.setting_record import SettingRecord
from src.data_transfer.selection.discrete_option import DiscreteOption
from src.model.analysis_structure.spatial_analysis.path_daytime_analysis import PathDaytimeAnalysis
from src.model.analysis_structure.spatial_analysis.path_time_analysis import PathTimeAnalysis
from src.model.analysis_structure.spatial_analysis.source_destination_analysis import SourceDestinationAnalysis
from src.model.polygon_structure.ipolygon_structure import IPolygonStructure


def get_time_list(step: int, size: int, start: int = 40000):
    """
    Creates a list of timestamps from the parameters in the format hh:mm:ss
    :param step: The steps the time takes between each timestamp.
    :param size: How many timestamps will be returned.
    :param start: Where the first time stamp start given as seconds of the day.
    :return: a list of timestamps
    """
    time_int = start
    time_list = [time.strftime('%H:%M:%S', time.gmtime(time_int + i * step)) for i in range(size)]
    return time_list


class Trajectory:
    """
    A helper class for generating the data for the analyses. It creates all the data of a trajectory.
    """

    def __init__(self, points: List[Tuple[float, float]], identifier):
        """
        sets the parameters
        :param points: the points are in the format: (longitude, latitude)
        """
        self._points = points
        self._id = identifier

    def get_longitude_list(self):
        return [point[0] for point in self._points]

    def get_latitude_list(self):
        return [point[1] for point in self._points]

    def get_points_len(self):
        return len(self._points)

    def get_id_list(self):
        return [self._id] * self.get_points_len()


class StartEndTest(unittest.TestCase):

    def setUp(self) -> None:
        """
        Sets up the necessary data for the analyses.
        :return:
        """
        self.start_polygon = PolygonRecord((Point(_longitude=8.3946276, _latitude=49.0153982),
                                            Point(_longitude=8.3947563, _latitude=49.0171573),
                                            Point(_longitude=8.39849, _latitude=49.017101),
                                            Point(_longitude=8.398447, _latitude=49.0152293)),
                                           _name="start_polygon")
        self.end_polygon = PolygonRecord((Point(_longitude=8.4212244, _latitude=49.018642),
                                          Point(_longitude=8.4248829, _latitude=49.0197466),
                                          Point(_longitude=8.4241211, _latitude=49.0215478),
                                          Point(_longitude=8.4206343, _latitude=49.0204995)),
                                         _name="start_polygon")
        self.trajectories = [
            Trajectory([(8.3932972, 49.0175584),  # Trajectory starts before start polygon
                        (8.3969879, 49.0157360),
                        (8.3998632, 49.0114013),
                        (8.4074378, 49.0113872),
                        (8.4102058, 49.0092619),
                        (8.4172869, 49.0091212),
                        (8.4231234, 49.0113168),
                        (8.4216428, 49.0196200)], "id1"),

            Trajectory([(8.3961940, 49.0159048),
                        (8.3981895, 49.0146805),
                        (8.4001422, 49.0112887),
                        (8.4054208, 49.0102190),
                        (8.4082747, 49.0110072),
                        (8.4101629, 49.0093464),
                        (8.4172225, 49.0090930),
                        (8.4182310, 49.0134138),
                        (8.4227157, 49.0134138),
                        (8.4213853, 49.0194933)], "id2"),

            Trajectory([(8.4222865, 49.0200281),  # Wrong trajectory in the wrong direction
                        (8.4044766, 49.0142020),
                        (8.3968806, 49.0157360)], "id3"),

            Trajectory([(8.3959365, 49.0160456),
                        (8.3979964, 49.0157500),
                        (8.3967733, 49.0233067),
                        (8.4055495, 49.0241931),
                        (8.4104419, 49.0231097),
                        (8.4153771, 49.0202813),
                        (8.4204626, 49.0231660),
                        (8.4214497, 49.0195215)], "id4")  # quickest way according to Apple Maps: 3,4km
        ]

        self.data_df: pd.DataFrame = pd.DataFrame({Column.TRAJECTORY_ID.value: [trajectory_id for idlist in
                                                                                [trajectory.get_id_list()
                                                                                 for trajectory
                                                                                 in self.trajectories]
                                                                                for trajectory_id
                                                                                in idlist],
                                                   Column.LONGITUDE.value: [long for long_list in
                                                                            [trajectory.get_longitude_list()
                                                                             for trajectory
                                                                             in self.trajectories]
                                                                            for long
                                                                            in long_list],
                                                   Column.LATITUDE.value: [lat for lat_list in
                                                                           [trajectory.get_latitude_list()
                                                                            for trajectory
                                                                            in self.trajectories]
                                                                           for lat
                                                                           in lat_list],
                                                   Column.DATE.value: ["31.01.2023"] * sum([trajectory.get_points_len()
                                                                                            for trajectory
                                                                                            in self.trajectories]),
                                                   Column.TIME.value: [time_val for time_list in
                                                                       [get_time_list(5, trajectory.get_points_len())
                                                                        for trajectory
                                                                        in self.trajectories]
                                                                       for time_val
                                                                       in time_list]})

        self.analysis_record: AnalysisRecord = AnalysisRecord(
            _required_data=(
                SettingRecord(
                    _identifier="",

                    _context="start and end polygon",
                    _selection=SelectionRecord(
                        selected=[self.start_polygon, self.end_polygon],
                        option=DiscreteOption([self.start_polygon, self.end_polygon]),
                        possible_selection_range=range(2, 3)
                    )
                ),
            )
        )

    def test_analysis_path_time(self):
        """
        Tests the path time analysis by comparing it against the expected result.
        """
        analysis = PathTimeAnalysis()
        analysis.set_analysis_parameters(self.analysis_record)

        result = analysis.analyse(self.data_df)
        del self.trajectories[2]
        expected_result = pd.DataFrame({
            'time': [delta_time for time_list in
                     [[i * 5.0 for i in range(trajectory.get_points_len())]
                      for trajectory in self.trajectories]
                     for delta_time in time_list],
            'distance': [0.0, 337.28, 863.51, 1416.58, 1727.74, 2245.03, 2736.31, 3666.92,
                         0.0, 199.5, 603.1, 1006.5, 1232.6, 1463.23, 1979.48, 2466.08, 2793.52, 3477.22,
                         0.0, 153.95, 999.89, 1648.08, 2025.03, 2503.5, 2994.36, 3406.41]

        })

        self.assertDictEqual(expected_result.to_dict(), result.data.data.to_dict())

    def test_analysis_source_destination(self):
        """
        Tests the source destination analysis by comparing it against the expected result.
        """
        analysis = SourceDestinationAnalysis()
        analysis.set_analysis_parameters(self.analysis_record)
        result = analysis.analyse(self.data_df)
        expected_result = pd.DataFrame({
            Column.TRAJECTORY_ID.value: ['id1', 'id2', 'id4', 'mean'],
            'time': ['00:00:35', '00:00:45', '00:00:35', '00:00:38'],
            'distance': [3667.0, 3477.0, 3406.0, 3517.0],
            'average_speed': [377.0, 278.0, 350.0, 330.0]})
        self.assertDictEqual(expected_result.to_dict(), result.data.data.to_dict())

    def test_analysis_path_daytime(self):
        """
        Tests the path daytime analysis by comparing it against the expected result.
        """
        analysis = PathDaytimeAnalysis()
        analysis.set_analysis_parameters(self.analysis_record)
        result = analysis.analyse(self.data_df)
        expected_result = pd.DataFrame({
            Column.TRAJECTORY_ID.value: ['id1'] * 8 + ['id2'] * 10 + ['id4'] * 8,
            Column.TIME.value: ['11:06:40', '11:06:45', '11:06:50', '11:06:55', '11:07:00', '11:07:05', '11:07:10',
                                '11:07:15',
                                '11:06:40', '11:06:45', '11:06:50', '11:06:55', '11:07:00', '11:07:05',
                                '11:07:10', '11:07:15', '11:07:20', '11:07:25',
                                '11:06:40', '11:06:45', '11:06:50', '11:06:40', '11:06:45', '11:06:50', '11:06:55',
                                '11:07:00'],
            'distance': [0.0, 337.28, 863.51, 1416.58, 1727.74, 2245.03, 2736.31, 3666.92,
                         0.0, 199.5, 603.1, 1006.5, 1232.6, 1463.23, 1979.48, 2466.08, 2793.52, 3477.22,
                         0.0, 153.95, 999.89, 1648.08, 2025.03, 2503.5, 2994.36, 3406.41]
        })
        self.assertDictEqual(expected_result.to_dict(), result.data.data.to_dict())


class ConsumerTest(unittest.TestCase):
    def setUp(self) -> None:
        self.start_end_analysis = PathTimeAnalysis()
        self.polygon_structure = Mock(IPolygonStructure)

    def test_set_polygon_structure_with_zero_polygons(self):
        self.polygon_structure.get_all_polygons.return_value = []

        with self.assertRaises(ValueError):
            self.start_end_analysis.set_polygon_structure(self.polygon_structure)

    def test_set_polygon_structure_with_one_polygon(self):
        self.polygon_structure.get_all_polygons.return_value = [1]
        expected_record = AnalysisRecord(
            _required_data=(
                SettingRecord(
                    _context="start and end polygon",
                    _selection=SelectionRecord(
                        selected=[1, 1],
                        option=DiscreteOption([1, 1]),
                        possible_selection_range=range(2, 3)
                    )
                ),
            ),
        )
        self.start_end_analysis.set_polygon_structure(self.polygon_structure)
        self.assertEqual(self.start_end_analysis.get_required_analysis_parameter(), expected_record)

    def test_set_polygon_structure_with_multiple_polygons(self):
        self.polygon_structure.get_all_polygons.return_value = [1, 2, 3]
        expected_record = AnalysisRecord(
            _required_data=(
                SettingRecord(
                    _context="start and end polygon",
                    _selection=SelectionRecord(
                        selected=[1, 2],
                        option=DiscreteOption([1, 2, 3]),
                        possible_selection_range=range(2, 3)
                    )
                ),
            ),
        )
        self.start_end_analysis.set_polygon_structure(self.polygon_structure)
        self.assertEqual(self.start_end_analysis.get_required_analysis_parameter(), expected_record)


if __name__ == '__main__':
    unittest.main()
