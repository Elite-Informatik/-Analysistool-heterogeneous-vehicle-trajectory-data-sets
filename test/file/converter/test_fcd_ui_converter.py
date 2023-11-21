import unittest
from typing import List
from unittest import TestCase
from uuid import UUID

import pandas as pd
from dateutil.parser import ParserError
from pandas import DataFrame

from src.data_transfer.content import Column
from src.data_transfer.content.road_type import VehicleType
from src.file.converter.fcd_ui_handler.fcd_columns import FcdColumn
from src.file.converter.fcd_ui_handler.fcd_ui_handler import AccelerationCalculator
from src.file.converter.fcd_ui_handler.fcd_ui_handler import AccelerationDirectionCalculator
from src.file.converter.fcd_ui_handler.fcd_ui_handler import DateCalculator
from src.file.converter.fcd_ui_handler.fcd_ui_handler import GpsCoordinateCalculator
from src.file.converter.fcd_ui_handler.fcd_ui_handler import IdCalculator
from src.file.converter.fcd_ui_handler.fcd_ui_handler import OSMRoadIDCalculator
from src.file.converter.fcd_ui_handler.fcd_ui_handler import OneWayStreetCalculator
from src.file.converter.fcd_ui_handler.fcd_ui_handler import RoadTypeCalculator
from src.file.converter.fcd_ui_handler.fcd_ui_handler import SpeedCalculator
from src.file.converter.fcd_ui_handler.fcd_ui_handler import SpeedDirectionCalculator
from src.file.converter.fcd_ui_handler.fcd_ui_handler import SpeedLimitCalculator
from src.file.converter.fcd_ui_handler.fcd_ui_handler import TimeCalculator
from src.file.converter.fcd_ui_handler.fcd_ui_handler import TrajectoryIDCalculator
from src.file.converter.fcd_ui_handler.fcd_ui_handler import VehicleTypeCalculator


class FcdUiConverterTest(TestCase):

    def test_trajectory_id_calculator(self):
        source_df = DataFrame({FcdColumn.TRIP.value: [1, "-5", "test1", -5, "test2"]})
        source_df = source_df.astype(str)
        new_data_frame = DataFrame()
        converter = TrajectoryIDCalculator()

        self.assertTrue(converter.is_repairable(source_df))
        self.assertEqual(converter.find_fatal_corruptions(source_df), [4])
        self.assertEqual(converter.find_repairable_corruptions(source_df), [2])
        source_df.drop(index=[4], inplace=True)
        self.assertTrue(source_df.equals(DataFrame({FcdColumn.TRIP.value: ["1", "-5", "test1", "-5"]})))
        converter.repair_column(source_df)
        self.assertTrue(source_df.equals(DataFrame({FcdColumn.TRIP.value: ["1", "-5", "-5", "-5"]})))
        converter.calculate_column(source_df, new_data_frame)
        # assert that the generated the same uuid for each trajectory id
        self.assertIsInstance(new_data_frame[Column.TRAJECTORY_ID.value][0], UUID)
        second_trajectory_id = new_data_frame[Column.TRAJECTORY_ID.value][1]
        # assert that the generated the same uuid for the last 3 trajectory ids
        for trajectory_id in new_data_frame[Column.TRAJECTORY_ID.value][1:4]:
            self.assertEqual(second_trajectory_id, trajectory_id)

    def test_gps_calculator(self):
        source_df = DataFrame(
            {FcdColumn.POINT.value: ["POINT (8.700645 50.112865)", "POINT (8.1 50.5)", "Point (6.1 5.3)"]})
        source_df = source_df.astype(str)
        new_data_frame = DataFrame()
        converter = GpsCoordinateCalculator()

        self.assertTrue(converter.is_repairable(source_df))
        self.assertEqual(converter.find_fatal_corruptions(source_df), [2])
        self.assertEqual(converter.find_repairable_corruptions(source_df), [])
        source_df.drop(index=[2], inplace=True)
        self.assertTrue(
            source_df.equals(DataFrame({FcdColumn.POINT.value: ["POINT (8.700645 50.112865)", "POINT (8.1 50.5)"]})))
        converter.repair_column(source_df)
        self.assertTrue(
            source_df.equals(DataFrame({FcdColumn.POINT.value: ["POINT (8.700645 50.112865)", "POINT (8.1 50.5)"]})))
        converter.calculate_column(source_df, new_data_frame)
        expected_df = DataFrame({Column.LONGITUDE.value: [float(8.700645), float(8.1)],
                                 Column.LATITUDE.value: [float(50.112865), float(50.5)]})
        self.assertTrue(new_data_frame.equals(expected_df))

    def test_road_type_calculator(self):
        test_df = DataFrame({FcdColumn.ROAD_TYPE.value: ["", None]})
        source_df = DataFrame({FcdColumn.ROAD_TYPE.value: ["motorway", '', 5]})
        source_df = source_df.astype(str)
        new_data_frame = DataFrame()
        converter = RoadTypeCalculator()
        self.assertFalse(converter.is_repairable(test_df))
        self.assertTrue(converter.is_repairable(source_df))
        self.assertEqual(converter.find_fatal_corruptions(source_df), [])
        self.assertEqual(converter.find_repairable_corruptions(source_df), [1])
        source_df.drop(index=[], inplace=True)
        # source_df.reset_index(drop=True, inplace=True)
        # expected_df = DataFrame({FcdColumn.ROAD_TYPE.value: ["motorway", "motorway", "5"]})
        # self.assertTrue(source_df.equals(expected_df))
        converter.repair_column(source_df)
        self.assertTrue(source_df.equals(DataFrame({FcdColumn.ROAD_TYPE.value: ["motorway", "motorway", "5"]})))
        converter.calculate_column(source_df, new_data_frame)
        expected_df = DataFrame({Column.ROAD_TYPE.value: ["motorway", "motorway", "5"]})
        self.assertTrue(new_data_frame.equals(expected_df))

    def test_speed_direction_calculator(self):
        source_df = DataFrame(
            {FcdColumn.POINT.value: ["POINT (9.0 50.0)", "POINT (8.0 50.0)"], FcdColumn.AZIMUTH.value: [35, ""]})
        source_df = source_df.astype(str)
        new_data_frame = DataFrame()
        converter = SpeedDirectionCalculator()

        self.assertTrue(converter.is_repairable(source_df))
        self.assertEqual(converter.find_fatal_corruptions(source_df), [])
        self.assertEqual(converter.find_repairable_corruptions(source_df), [])
        # source_df.drop(index=[], inplace=True)
        # source_df.reset_index(drop=True, inplace=True)
        # expected_df = DataFrame({FcdColumn.ROAD_TYPE.value: ["motorway", "5"]})
        # self.assertTrue(source_df.equals(expected_df))
        converter.repair_column(source_df)
        self.assertDictEqual(source_df.to_dict(), DataFrame(
            {FcdColumn.POINT.value: ["POINT (9.0 50.0)", "POINT (8.0 50.0)"]
                , FcdColumn.AZIMUTH.value: [35.0, 90.0]})
                             .to_dict())
        converter.calculate_column(source_df, new_data_frame)
        expected_df = DataFrame({Column.SPEED_DIRECTION.value: [35.0, 90.0]})
        self.assertTrue(new_data_frame.equals(expected_df))

    def test_osm_road_id_calculator(self):
        source_df = DataFrame({FcdColumn.ROAD_OSM_TYPE.value: [512, "test", 420]})
        source_df = source_df.astype(str)
        new_data_frame = DataFrame()
        converter = OSMRoadIDCalculator()

        self.assertTrue(converter.is_repairable(source_df))
        self.assertEqual(converter.find_fatal_corruptions(source_df), [])
        self.assertEqual(converter.find_repairable_corruptions(source_df), [1])
        converter.repair_column(source_df)
        self.assertTrue(source_df.equals(DataFrame(
            {FcdColumn.ROAD_OSM_TYPE.value: ["512", "512", "420"]})))
        converter.calculate_column(source_df, new_data_frame)
        expected_df = DataFrame({Column.OSM_ROAD_ID.value: [512, 512, 420]})
        self.assertDictEqual(expected_df.to_dict(), new_data_frame.to_dict())

    def test_acceleration_direction_calculator(self):
        source_df = DataFrame(
            {FcdColumn.SPEED.value: [50, 50, 0], FcdColumn.AZIMUTH.value: [0, 90, 0]})
        new_data_frame = DataFrame()
        converter = AccelerationDirectionCalculator()

        self.assertTrue(converter.is_repairable(source_df))
        self.assertEqual(converter.find_fatal_corruptions(source_df), [])
        self.assertEqual(converter.find_repairable_corruptions(source_df), [])
        converter.calculate_column(source_df, new_data_frame)
        expected_df = DataFrame({Column.ACCELERATION_DIRECTION.value: [135.0, 270.0, 0.0]})
        self.assertTrue(new_data_frame.equals(expected_df))


class IdTest(TestCase):
    """
    Test class for the IdCalculator class.
    """

    def setUp(self) -> None:
        """
        Sets up the test case. Creates a converter and a source DataFrame, which is used to test the converter.
        :return:
        """
        self.converter = IdCalculator()
        self.source_df = DataFrame({FcdColumn.TRIP.value: [1, 5, 3]})
        self.result_df = DataFrame()

    def test_id_calculator(self):
        """
        Tests the id calculator. Checks if the id is a UUID.
        """
        self.converter.calculate_column(source_df=self.source_df, result_df=self.result_df)
        for i, id in enumerate(self.result_df[Column.ID.value].to_list()):
            with self.subTest(i=i):
                self.assertIsInstance(id, UUID)

    def test_find_repairable_corruptions(self):
        """
        Tests the find_repairable_corruptions method. Checks if the method returns an empty list.
        """
        self.assertEqual(self.converter.find_repairable_corruptions(self.source_df), [])

    def test_find_fatal_corruptions(self):
        """
        Tests the find_fatal_corruptions method. Checks if the method returns an empty list.
        """
        self.assertEqual(self.converter.find_fatal_corruptions(self.source_df), [])

    def test_is_repairable(self):
        """
        Tests the is_repairable method. Checks if the method returns True.
        """
        self.assertTrue(self.converter.is_repairable(self.source_df))

    def test_repairable_corruptions(self):
        """
        Tests the repair_column method. Checks if the method returns the same DataFrame.
        """
        self.assertTrue(self.converter.repair_column(self.source_df))


class DateTimeTest(TestCase):
    """
    Test class for the DateCalculator and TimeCalculator classes.
    """

    def test_fcd_date_time(self):
        """

        :return:
        """
        source_data = DataFrame({FcdColumn.DATE_TIME.value: ['2021-09-16T04:38:11.000Z',
                                                             '2021-09-16T04:38:15.000Z',
                                                             '2021-09-16T04:38:16.000Z',
                                                             '2021-09-16T04:38:20.000Z'],
                                 FcdColumn.TRIP.value: [1, 1, 1, 1]})
        result_data = DataFrame()
        date_converter = DateCalculator()
        time_converter = TimeCalculator()
        # assert that the column returns true when calculated
        self.assertTrue(date_converter.calculate_column(source_df=source_data, result_df=result_data))
        self.assertTrue(time_converter.calculate_column(source_df=source_data, result_df=result_data))

        # assert the time and date columns are added to the result dataframe correctly in format
        # DD.MM.YYYY and HH:MM:SS
        self.assertTrue(result_data.equals(DataFrame({
            Column.DATE.value: ['16.09.2021', '16.09.2021', '16.09.2021', '16.09.2021'],
            Column.TIME.value: ['04:38:11', '04:38:15', '04:38:16', '04:38:20']})))

    def test_fcd_date_time_invalid_convertable(self):
        """
        Tests the date and time calculator with invalid data, which can be repaired.
        """
        source_data = DataFrame({FcdColumn.DATE_TIME.value: ['2021-09-16T04:38:11.000Z',
                                                             '2021-09-16T04:38:15.000Z',
                                                             'invalid',
                                                             '2021-09-16T04:38:20.000Z'],
                                 FcdColumn.TRIP.value: [1, 1, 1, 1]})
        result_data = DataFrame()
        date_converter = DateCalculator()
        time_converter = TimeCalculator()

        # assert that a ParserError is raised when the column is calculated and not repaired beforehand
        self.assertRaises(ValueError, date_converter.calculate_column, source_df=source_data,
                          result_df=result_data)
        self.assertRaises(ValueError, time_converter.calculate_column, source_df=source_data, result_df=result_data)

        # assert that the column is repairable and that no fatal corruptions are found
        self.assertTrue(date_converter.is_repairable(source_df=source_data))
        self.assertTrue(time_converter.is_repairable(source_df=source_data))

        self.assertListEqual([], date_converter.find_fatal_corruptions(source_df=source_data))
        self.assertListEqual([], time_converter.find_fatal_corruptions(source_df=source_data))

        # assert that the column is repaired correctly
        date_converter.repair_column(source_df=source_data)
        self.assertTrue(date_converter.calculate_column(source_df=source_data, result_df=result_data))
        self.assertTrue(time_converter.calculate_column(source_df=source_data, result_df=result_data))

        # assert that the result dataframe is correct
        self.assertEquals(DataFrame({Column.DATE.value: ['16.09.2021', '16.09.2021', '16.09.2021',
                                                         '16.09.2021'],
                                     Column.TIME.value: ['04:38:11', '04:38:15', '04:38:17',
                                                         '04:38:20']}).to_dict(), result_data.to_dict())

    def test_fcd_date_time_get_corrupt(self):
        """
        Tests the find_fatal_corruptions method of the date and time calculator.
        """
        # create a list of invalid dataframes
        invalid_data: List[pd.DataFrame] = [DataFrame({FcdColumn.DATE_TIME.value: ['2021-09-16T04:38:11.000Z',
                                                                                   '2021-09-16:38:15.000Z',
                                                                                   '2021-09-16:38:15.000Z',
                                                                                   '2021-09-16T04:38:20.000Z'],
                                                       FcdColumn.TRIP.value: [1, 1, 1, 1]}),
                                            DataFrame({FcdColumn.DATE_TIME.value: ['2021-09-16T04:38:11.000Z',
                                                                                   '2021-09-16T04:a:15.000Z',
                                                                                   'invalid',
                                                                                   '2021-09-16T04:38:20.000Z'],
                                                       FcdColumn.TRIP.value: [1, 1, 1, 1]}),
                                            DataFrame({FcdColumn.DATE_TIME.value: ['2021-09-16T04:38:11.000Z',
                                                                                   '2021-09-16T04:38:15.000Z',
                                                                                   'invalid',
                                                                                   '2021-09-16T04:38:20.000Z'],
                                                       FcdColumn.TRIP.value: [1, 1, 2, 2]}),
                                            DataFrame({FcdColumn.DATE_TIME.value: ['2021-09-16T04:38:11.000Z',
                                                                                   '2021-09-16T04:38:15.000Z',
                                                                                   'invalid',
                                                                                   '2021-09-16Ta4:38:20.000Z'],
                                                       FcdColumn.TRIP.value: [1, 1, 2, 2]}),
                                            DataFrame({FcdColumn.DATE_TIME.value: ['2021-09-16T04:38:11.000Z',
                                                                                   '2021-09-16T04:38:15.000Z',
                                                                                   'invalid',
                                                                                   '2021-09-16Ta4:38:20.000Z',
                                                                                   '2021-09-16T04:38:15.000Z'],
                                                       FcdColumn.TRIP.value: [1, 1, 2, 2, 3]})
                                            ]
        # create a list of the indexes of expected fatal errors for each dataframe
        fatal_errors: List[List[int]] = [
            [1],
            [1],
            [2],
            [2, 3],
            [2, 3]
        ]

        for i, source_data in enumerate(invalid_data):
            with self.subTest(i=i):
                result_data = DataFrame()
                date_converter = DateCalculator()
                time_converter = TimeCalculator()
                # assert that a ParserError is raised when the column is calculated and not repaired beforehand
                self.assertRaises(ValueError, date_converter.calculate_column, source_df=source_data,
                                  result_df=result_data)

                # assert that the column is repairable and that the correct fatal corruptions are found
                self.assertTrue(date_converter.is_repairable(source_df=source_data))
                self.assertListEqual(fatal_errors[i], date_converter.find_fatal_corruptions(source_df=source_data))

                self.assertRaises(ValueError, time_converter.calculate_column, source_df=source_data,
                                  result_df=result_data)
                self.assertTrue(time_converter.is_repairable(source_df=source_data))
                self.assertListEqual(fatal_errors[i], date_converter.find_fatal_corruptions(source_df=source_data))

    def test_find_repairable_corruptions(self):
        """
        Tests if the find_repairable_corruptions method works as expected
        """
        source_data = DataFrame({FcdColumn.DATE_TIME.value: ['2021-09-16T04:38:11.000Z',
                                                             '2021-09-16T04:38:15.000Z',
                                                             'invalid',
                                                             '2021-09-16T04:38:20.000Z'],
                                 FcdColumn.TRIP.value: [1, 1, 1, 1]})
        result_data = DataFrame()
        date_converter = DateCalculator()
        time_converter = TimeCalculator()
        self.assertRaises(ValueError, date_converter.calculate_column, source_df=source_data,
                          result_df=result_data)
        self.assertTrue(date_converter.is_repairable(source_df=source_data))
        self.assertListEqual([2], date_converter.find_repairable_corruptions(source_df=source_data))

        self.assertRaises(ValueError, time_converter.calculate_column, source_df=source_data, result_df=result_data)
        self.assertTrue(time_converter.is_repairable(source_df=source_data))
        self.assertListEqual([2], time_converter.find_repairable_corruptions(source_df=source_data))


class SpeedLimitTest(TestCase):
    """
    Tests the speed limit calculator
    """

    def setUp(self) -> None:
        """
        Sets up the test case by creating a speed limit calculator and a list of dataframes.
        """
        self.column = FcdColumn.MAX_SPEED.value

        # create a list of dataframes with different values for the speed limit column
        self.dataframes: [DataFrame] = [
            DataFrame({self.column: [30, "a", "20", 40, None, 50], FcdColumn.ROAD_TYPE.value: ["fast"] * 6}),

            DataFrame({self.column: ["a", "a", "20", "a", None, None], FcdColumn.ROAD_TYPE.value: ["fast"] * 6}),

            DataFrame({self.column: ["20", "a", "a", "100", None, None],
                       FcdColumn.ROAD_TYPE.value: ["slow"] * 3 + ["fast"] * 3}),

            DataFrame({self.column: ["a", "1", "a", "30", None, "100"],
                       FcdColumn.ROAD_TYPE.value: ["slow"] * 3 + ["fast"] * 3}),

            pd.DataFrame({self.column: [30, "a", "20", None, None, None], FcdColumn.ROAD_TYPE.value: ["fast"] * 6}),

            pd.DataFrame({self.column: ["a", "a", "a", "30", None, "100"],
                          FcdColumn.ROAD_TYPE.value: ["slow"] * 3 + ["fast"] * 3})
        ]

        # create a list of the expected values for the speed limit column
        self.expected_limits: List[List[float]] = [
            [30.0, 30.0, 20.0, 40.0, 40.0, 50.0],
            [20.0] * 6,
            [20.0] * 3 + [100.0] * 3,
            [1.0] * 3 + [30.0, 30.0, 100.0],
            [30.0, 30.0] + [20.0] * 4,
            [30] * 5 + [100]
        ]

        # create a list of the indexes of expected fatal errors for each dataframe
        self.illegal_lines: List[List[float]] = [
            [],
            [],
            [],
            [],
            [],
            [0, 1, 2]
        ]

        # create a list of the indexes of expected repairable errors for each dataframe
        self.repairable_lines: List[List[int]] = [
            [1, 4],
            [0, 1, 3, 4, 5],
            [1, 2, 4, 5],
            [0, 2, 4],
            [1, 3, 4, 5],
            [0, 1, 2, 4]
        ]
        self.calculator = SpeedLimitCalculator()

    def test_fcd_speed_limit_repair(self):
        """
        Tests if the speed limit calculator can repair the speed limit column.
        After repairing the column, the fatal corruptions should be empty and the speed limit column should be correct.
        """
        for i, source_df in enumerate(self.dataframes):
            self.assertTrue(self.calculator.is_repairable(source_df=source_df))
            self.calculator.repair_column(source_df=source_df)
            self.assertListEqual([], self.calculator.find_fatal_corruptions(source_df=source_df))
            self.assertListEqual(self.expected_limits[i], source_df[FcdColumn.MAX_SPEED.value].to_list())

    def test_find_corruptions_speed_limit(self):
        """
        Tests if the find_fatal_corruptions finds all fatal corruptions and if the find_repairable_corruptions finds all
        repairable corruptions.
        """
        for i, source_df in enumerate(self.dataframes):
            self.assertTrue(self.calculator.is_repairable(source_df=source_df))
            self.assertListEqual(self.repairable_lines[i],
                                 self.calculator.find_repairable_corruptions(source_df=source_df))
            self.assertListEqual(self.illegal_lines[i], self.calculator.find_fatal_corruptions(source_df=source_df))

    def test_calculate_column(self):
        """
        Tests if the speed limit calculator can calculate the speed limit column correctly.
        """
        for dataset in self.dataframes:
            result = DataFrame()
            self.calculator.calculate_column(source_df=dataset, result_df=result)
            self.assertDictEqual(dataset[self.column].to_dict(), result[Column.SPEED_LIMIT.value].to_dict())

    def test_not_repairable(self):
        """
        Tests if the speed limit calculator can detect if a dataframe is not repairable.
        """
        not_repairable = [
            DataFrame(),
            DataFrame({"random column": ["random value"]}),
            DataFrame({self.column: [100, 100]}),
            DataFrame({FcdColumn.ROAD_TYPE.value: ["SPEED", "sped"]}),
            DataFrame({self.column: ["invalid", "values"],
                       FcdColumn.ROAD_TYPE.value: ["speed", "road"]})
        ]

        for dataframe in not_repairable:
            self.assertFalse(self.calculator.is_repairable(dataframe))


class SpeedCalculatorTest(TestCase):
    """
    Tests the speed calculator.
    """

    def setUp(self) -> None:
        """
        Sets up the test data.
        """
        # create a list of dataframes that should be able to be repaired
        self.valid_speed_dfs = [DataFrame({FcdColumn.SPEED.value: [20, 30, 30, 50, 60]}),
                                DataFrame({FcdColumn.SPEED.value: [20, None, None, None, 60]}),
                                DataFrame({FcdColumn.SPEED.value: [None, 30, None, 50, 60]}),
                                DataFrame({FcdColumn.SPEED.value: [20, 30, None, None, None]}),
                                DataFrame({
                                    FcdColumn.DATE_TIME.value: ['2021-09-16T04:38:11.000Z',
                                                                '2021-09-16T04:38:16.000Z',
                                                                '2021-09-16T04:38:21.000Z',
                                                                '2021-09-16T04:38:26.000Z',
                                                                '2021-09-16T04:38:31.000Z'],
                                    FcdColumn.POINT.value: ['POINT (8.530747 50.11433)',
                                                            'POINT (8.532227 50.11488)',
                                                            'POINT (8.534014 50.11552)',
                                                            'POINT (8.534918 50.115852)',
                                                            'POINT (8.53647 50.116417)'],
                                    FcdColumn.TRIP.value: [1] * 5
                                })
                                ]
        self.speed_calculator = SpeedCalculator()

        # create a list of expected speed values for each dataframe
        self.expected_complete = [
            [20.0, 30.0, 30.0, 50.0, 60.0],
            [20.0, 30.0, 40.0, 50.0, 60.0],
            [30.0, 30.0, 40.0, 50.0, 60.0],
            [20.0, 30.0, 30.0, 30.0, 30.0],
            [87.9, 87.9, 105.2, 53.5, 91.7]
        ]

        # create a list of expected repairable corruptions (lines) for each dataframe
        self.expected_repairable = [
            [],
            [1, 2, 3],
            [0, 2],
            [2, 3, 4],
            [0, 1, 2, 3, 4]
        ]

    def test_is_repairable(self):
        """
        Tests if the speed calculator can detect if a dataframe is repairable.
        """
        for df in self.valid_speed_dfs:
            self.assertTrue(self.speed_calculator.is_repairable(df))

    def test_fatal_corruptions(self):
        for df in self.valid_speed_dfs:
            self.assertListEqual([], self.speed_calculator.find_fatal_corruptions(df))

    def test_repairable_corruptions(self):
        for ex_result, df in zip(self.expected_repairable, self.valid_speed_dfs):
            self.assertListEqual(ex_result, self.speed_calculator.find_repairable_corruptions(df))

    def test_repair(self):
        for ex_result, df in zip(self.expected_complete, self.valid_speed_dfs):
            self.speed_calculator.repair_column(df)
            self.assertListEqual(ex_result, df[FcdColumn.SPEED.value].to_list())

        source_df = DataFrame({
            FcdColumn.DATE_TIME.value: ['2021-09-16T04:38:11.000Z', '2021-09-16T04:38:16.000Z',
                                        '2021-09-16T04:38:21.000Z',
                                        '2021-09-16T04:38:26.000Z'],
            FcdColumn.POINT.value: ['POINT (8.530747 50.11433)', 'POINT (8.532227 50.11488)',
                                    'POINT (8.534014 50.11552)',
                                    'POINT (8.534918 50.115852)'],
            FcdColumn.TRIP.value: [1, 1, 1, 1]
        })
        self.speed_calculator.repair_column(source_df)

    def test_calculate_column(self):
        """
        Test that the speed column is calculated correctly.
        """
        for df, expected in zip(self.valid_speed_dfs, self.expected_complete):
            result = DataFrame()
            self.speed_calculator.repair_column(df)
            self.speed_calculator.calculate_column(df, result)
            self.assertListEqual(expected, result[Column.SPEED.value].to_list())

    def test_not_repairable(self):
        # Test that if a dataset is not repairable the SpeedCalculator returns false.
        not_repairable = [
            # No trip column
            DataFrame({FcdColumn.DATE_TIME.value: ['2021-09-16T04:38:11.000Z', '2021-09-16T04:38:16.000Z',
                                                   '2021-09-16T04:38:21.000Z',
                                                   '2021-09-16T04:38:26.000Z'],
                       FcdColumn.POINT.value: ['POINT (8.530747 50.11433)', 'POINT (8.532227 50.11488)',
                                               'POINT (8.534014 50.11552)',
                                               'POINT (8.534918 50.115852)']
                       }),
            # No date time column
            DataFrame({FcdColumn.POINT.value: ['POINT (8.530747 50.11433)', 'POINT (8.532227 50.11488)',
                                               'POINT (8.534014 50.11552)',
                                               'POINT (8.534918 50.115852)'],
                       FcdColumn.TRIP.value: [1, 1, 1, 1]
                       }),
            # No point column
            DataFrame({FcdColumn.DATE_TIME.value: ['2021-09-16T04:38:11.000Z', '2021-09-16T04:38:16.000Z',
                                                   '2021-09-16T04:38:21.000Z',
                                                   '2021-09-16T04:38:26.000Z'],
                       FcdColumn.TRIP.value: [1, 1, 1, 1]
                       }),
            # fully illegal speed column and not one of the others.
            DataFrame({FcdColumn.DATE_TIME.value: ['2021-09-16T04:38:11.000Z', '2021-09-16T04:38:16.000Z',
                                                   '2021-09-16T04:38:21.000Z',
                                                   '2021-09-16T04:38:26.000Z'],
                       FcdColumn.SPEED.value: ["illegal"] * 4
                       }),
        ]
        for df in not_repairable:
            self.assertFalse(self.speed_calculator.is_repairable(df))


class AccelerationCalculatorTest(TestCase):
    """
    Tests the acceleration calculator.
    """

    def setUp(self) -> None:
        """
        Sets up the test.
        """
        # create a list of valid dataframes
        self.valid_acceleration: [DataFrame] = [
            DataFrame({FcdColumn.DATE_TIME.value: ['2021-09-16T04:38:11.000Z', '2021-09-16T04:38:16.000Z',
                                                   '2021-09-16T04:38:21.000Z',
                                                   '2021-09-16T04:38:26.000Z'],
                       FcdColumn.SPEED.value: [86, 87, 88, 91],
                       FcdColumn.TRIP.value: [1] * 4}),
            DataFrame({FcdColumn.DATE_TIME.value: ['2021-09-16T04:38:11.000Z', '2021-09-16T04:38:16.000Z',
                                                   '2021-09-16T04:38:21.000Z',
                                                   '2021-09-16T04:38:26.000Z'],
                       FcdColumn.SPEED.value: [86, 87, 88, 91],
                       FcdColumn.TRIP.value: [1] * 2 + [2] * 2})
        ]

        # create a list of expected results
        self.expected_results = [
            [0.06, 0.06, 0.06, 0.17],
            [0.06, 0.06, 0.17, 0.17]
        ]
        self.calculator: AccelerationCalculator = AccelerationCalculator()

    def test_calculation(self):
        """
        Test that the acceleration is calculated correctly.
        """
        for data_df, expected_result in zip(self.valid_acceleration, self.expected_results):
            result_df = DataFrame()
            self.calculator.calculate_column(source_df=data_df, result_df=result_df)
            self.assertListEqual([round(num, 2) for num in expected_result],
                                 [round(num, 2) for num in result_df[Column.ACCELERATION.value].to_list()])

    def test_find_repairable(self):
        """
        Test that the find_repairable_corruptions method returns an empty list. This is because the acceleration column
        is always calculated and never read from the source.
        """
        for data_df in self.valid_acceleration:
            self.assertListEqual([], self.calculator.find_repairable_corruptions(data_df))

    def test_find_fatal(self):
        """
        Test that the find_fatal_corruptions method returns an empty list. This is because the acceleration column is
        always calculated and never read from the source.
        """
        for data_df in self.valid_acceleration:
            self.assertListEqual([], self.calculator.find_fatal_corruptions(data_df))

    def test_is_repairable(self):
        """
        Test that the is_repairable method returns True. It is always repairable because it is always calculated.
        """
        for data_df in self.valid_acceleration:
            self.assertTrue(self.calculator.is_repairable(data_df))

    def test_repair(self):
        """
        Test that the repair_column method returns True. It is always repairable because it is always calculated.
        """
        for data_df in self.valid_acceleration:
            self.assertTrue(self.calculator.repair_column(data_df))


class VehicleTypeCalculatorTest(TestCase):
    """
    Tests the vehicle type calculator.
    """

    def setUp(self) -> None:
        """
        Sets up the test. Dataframe is created with a trip column as this sets a length for the vehicle type column.
        The column is not used in the calculation.
        """
        self.calculator: VehicleTypeCalculator = VehicleTypeCalculator()
        self.data = DataFrame({FcdColumn.TRIP.value: ['', '', '', '']})

    def test_is_repairable(self):
        """
        Test that the is_repairable method returns True. It is always repairable because it is always calculated.
        """
        self.assertTrue(self.calculator.is_repairable(self.data))

    def test_find_repairable(self):
        """
        Test that the find_repairable_corruptions method returns an empty list. This is because the vehicle type column
        is always set and never read from the source.
        """
        self.assertListEqual([], self.calculator.find_repairable_corruptions(self.data))

    def test_find_fatal(self):
        """
        Test that the find_fatal_corruptions method returns an empty list. This is because the vehicle type column
        is always set and never read from the source.
        """
        self.assertListEqual([], self.calculator.find_fatal_corruptions(self.data))

    def test_repair(self):
        """
        Test that the repair_column method returns True. It is always repairable because it is always set.
        """
        self.assertTrue(self.calculator.repair_column(self.data))

    def test_calculation(self):
        """
        Test that the vehicle type is calculated correctly. The vehicle type is always set to UNKNOWN.
        """
        self.calculator.calculate_column(self.data, self.data)
        self.assertListEqual([VehicleType.UNKNOWN.value] * 4, self.data[Column.VEHICLE_TYPE.value].to_list())


class OneWayStreetCalculatorTest(TestCase):
    """
    Tests the one way street calculator.
    """

    def setUp(self) -> None:
        """
        Sets up the test. Dataframes are created with a one way street column with varying degrees of corruption.
        """
        # create a list of dataframes with varying degrees of corruption
        self.valid_one_way: [DataFrame] = [
            DataFrame({FcdColumn.ONE_WAY_STREET.value: [True, True, False, True]}),
            DataFrame({FcdColumn.ONE_WAY_STREET.value: [True, True, 'FALSE', True]}),
            DataFrame({FcdColumn.ONE_WAY_STREET.value: [True, 'invalid', 'FALSE', True]}),
            DataFrame({FcdColumn.ONE_WAY_STREET.value: [True, 'invalid', 'invalid', True]})
        ]

        # create a list of expected results
        self.expected_results = [
            [True, True, False, True],
            [True, True, False, True],
            [True, True, False, True],
            [True, True, True, True]
        ]

        # create a list of expected repairable corruptions (indexes) for each dataframe
        self.repairable_corruptions = [
            [],
            [2],
            [1, 2],
            [1, 2]
        ]
        self.calculator: OneWayStreetCalculator = OneWayStreetCalculator()

    def test_calculation(self):
        """
        Test that the one way street is calculated correctly. It is first repaired and then calculated.
        """
        for data_df, expected_result in zip(self.valid_one_way, self.expected_results):
            result_df = DataFrame()
            self.calculator.repair_column(source_df=data_df)
            self.calculator.calculate_column(source_df=data_df, result_df=result_df)
            self.assertListEqual(expected_result, result_df[Column.ONE_WAY_STREET.value].to_list())

    def test_find_repairable(self):
        """
        Tests if the find_repairable_corruptions method returns the correct indexes of repairable corruptions.
        """
        for expected_result, data_df in zip(self.repairable_corruptions, self.valid_one_way):
            self.assertListEqual(expected_result, self.calculator.find_repairable_corruptions(data_df))

    def test_find_fatal(self):
        """
        Tests if the find_fatal_corruptions method returns an empty list. This is because the one way street column is

        :return:
        """
        for data_df in self.valid_one_way:
            self.assertListEqual([], self.calculator.find_fatal_corruptions(data_df))

    def test_is_repairable(self):
        for data_df in self.valid_one_way:
            self.assertTrue(self.calculator.is_repairable(data_df))


if __name__ == '__main__':
    unittest.main()
