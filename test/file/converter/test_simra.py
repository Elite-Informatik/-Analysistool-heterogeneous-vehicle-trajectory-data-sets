import unittest
from abc import abstractmethod, ABC
from unittest import TestCase

import pandas as pd

from src.data_transfer.content import Column
from src.file.converter.bicycle_simra.simra_bicycle_handler import AbstractColumnCalculator, IDCalculator, \
    TimeCalculator, DateCalculator, LongitudeCalculator, LatitudeCalculator, SpeedCalculator
from src.file.converter.bicycle_simra.simra_bicycle_columns import SimraColumn

unittest.TestLoader.sortTestMethodsUsing = None


class AbstractColumnCalculatorTest(TestCase, ABC):

    def setUp(self) -> None:
        self.source_df_full = pd.DataFrame(
            {SimraColumn.LATITUDE.value: [1, 2, 3],
             SimraColumn.LONGITUDE.value: [4, 5, 6],
             SimraColumn.X.value: [5.0, 6.0, 7.0],
             SimraColumn.Y.value: [8.0, 9.0, 10.0],
             SimraColumn.Z.value: [11.0, 12.0, 13.0],
             SimraColumn.TIME_STAMP.value: [1611683945172, 1611683946172, 1611684745172],
             SimraColumn.ACC.value: [14.0, 15.0, 16.0],
             SimraColumn.A.value: [17.0, 18.0, 19.0],
             SimraColumn.B.value: [20.0, 21.0, 22.0],
             SimraColumn.C.value: [23.0, 24.0, 25.0]
             }
        )
        self.expected_df_full = pd.DataFrame(
            {
                Column.LATITUDE.value: [1, 2, 3],
                Column.LONGITUDE.value: [4, 5, 6],
                Column.DATE.value: ["26.01.2021", "26.01.2021", "26.01.2021"],
                Column.TIME.value: ['17:59:05', '17:59:06', "18:12:25"],

            }
        )
        self.source_df_realistic = pd.DataFrame(
            {SimraColumn.LATITUDE.value: [1, 2, None],
             SimraColumn.LONGITUDE.value: [4, 5, None],
             SimraColumn.X.value: [5.0, 6.0, 7.0],
             SimraColumn.Y.value: [8.0, 9.0, 10.0],
             SimraColumn.Z.value: [11.0, 12.0, 13.0],
             SimraColumn.TIME_STAMP.value: [1611683945172, 1611683946172, 1611683745172],
             SimraColumn.ACC.value: [14.0, 15.0, None],
             SimraColumn.A.value: [17.0, 18.0, 19.0],
             SimraColumn.B.value: [20.0, 21.0, 22.0],
             SimraColumn.C.value: [23.0, 24.0, 25.0]
             }
        )
        self.calculator: AbstractColumnCalculator = None
        self.result_df: pd.DataFrame = pd.DataFrame()
        self.column = None

    def test_is_repairable(self):
        # calculator is set for the subclasses.
        if self.calculator is None:
            return
        is_repairable = self.calculator.is_repairable(self.source_df_realistic)
        self.assertTrue(is_repairable)
        self.assertTrue(self.calculator.is_repairable(self.source_df_full))

    def test_find_repairable_corruptions(self):
        if self.calculator is None:
            return
        self.assertListEqual(self.calculator.find_repairable_corruptions(self.source_df_full), [])
        self.assertListEqual(self.calculator.find_repairable_corruptions(self.source_df_realistic), [])

    def test_find_fatal_corruptions(self):
        if self.calculator is None:
            return
        self.assertListEqual(self.calculator.find_fatal_corruptions(self.source_df_full), [])

    def test_repair_column(self):
        if self.calculator is None:
            return
        original_full_column_lat = self.source_df_full[SimraColumn.LATITUDE.value].copy()
        self.assertTrue(self.calculator.is_repairable(self.source_df_realistic))
        self.assertTrue(self.calculator.is_repairable(self.source_df_full))
        self.assertListEqual(self.source_df_full[SimraColumn.LATITUDE.value].to_list(),
                             original_full_column_lat.to_list())

    def test_calculate_column(self):
        if self.calculator is None:
            return
        self.test_repair_column()
        self.calculator.calculate_column(self.source_df_full, self.result_df)
        self.assertIsNotNone(self.result_df)
        self.assertListEqual(self.result_df[self.column].to_list(), self.expected_df_full[self.column].to_list())


class TimeCalculatorTest(AbstractColumnCalculatorTest):
    def setUp(self):
        super().setUp()
        self.calculator = TimeCalculator()
        self.column = Column.TIME.value


class DateCalculatorTest(AbstractColumnCalculatorTest):
    def setUp(self):
        super().setUp()
        self.calculator = DateCalculator()
        self.column = Column.DATE.value


class LatitudeCalculatorTest(AbstractColumnCalculatorTest):
    def setUp(self):
        super().setUp()
        self.calculator = LatitudeCalculator()
        self.column = Column.LATITUDE.value


class LongitudeCalculatorTest(AbstractColumnCalculatorTest):
    def setUp(self):
        super().setUp()
        self.calculator = LongitudeCalculator()
        self.column = Column.LONGITUDE.value


class SpeedCalculatorTest(TestCase):
    def setUp(self):
        super().setUp()
        self.calculator = SpeedCalculator()
        self.column = Column.SPEED

    def test_speed(self):
        speed_test_df = pd.DataFrame(
            {SimraColumn.LONGITUDE.value: [8.372944077710317,
                                           8.372803921999456,
                                           8.372512339634245,
                                           8.372374524602556,
                                           8.372002215674037,
                                           8.371863827201496,
                                           8.371490032322717,
                                           8.371408124564342],
             SimraColumn.LATITUDE.value: [49.0056021533148,
                                          49.00561575107167,
                                          49.00561822733732,
                                          49.00560989988381,
                                          49.005578062817726,
                                          49.00557873484146,
                                          49.00557171259497,
                                          49.00558677502405],
             SimraColumn.TIME_STAMP.value: [1632806105000,
                                            1632806106000,
                                            1632806110000,
                                            1632806115000,
                                            1632806116000,
                                            1632806120000,
                                            1632806121000,
                                            1632806125000,
                                            ]
             })
        result_df = pd.DataFrame()
        expected_df = pd.DataFrame(
            {Column.SPEED.value: [27.0,
                                  25.0,
                                  22.0,
                                  25.0,
                                  27.0,
                                  25.0,
                                  27.0,
                                  25.0,
                                  24.0]})
        self.calculator.calculate_column(speed_test_df, result_df)
        print(result_df[self.column.value].to_list())
        # self.assertListEqual(self.result_df[self.column].to_list(), [0, 0, 0])


