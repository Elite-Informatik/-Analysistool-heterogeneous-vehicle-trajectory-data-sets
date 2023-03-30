import unittest
from enum import Enum

import pandas as pd

from src.data_transfer.content import Column
from src.data_transfer.content.analysis_view import AnalysisViewEnum
from src.data_transfer.exception import InvalidInput
from src.data_transfer.record import AnalysisRecord
from src.data_transfer.record import DataRecord
from src.data_transfer.record import SettingRecord
from src.data_transfer.record.selection_record import SelectionRecord
from src.data_transfer.selection.discrete_option import DiscreteOption
from src.model.analysis_structure.concrete_analysis.histrogram_analysis import HistogramAnalysis


class RoadType(Enum):
    RESIDENTIAL = "residential"
    HIGH_WAY = "high way"
    GRAVEL = "gravel"


class TestHistogramAnalysis(unittest.TestCase):
    """
    A class for testing the HistogramAnalysis.
    """

    def setUp(self):
        """
        Sets up the tests by defining test data and the corresponding expected results. The expected results are the
        number of occurrences of each value in the data.
        """
        self.analysis = HistogramAnalysis()
        self.data = {
            Column.SPEED.value: [10, 20, 30, 40, 50, 50, 50, 40, 52, 100],
            Column.ACCELERATION.value: [1, 2, 3, 4, 3, 2, 2, 1, 1, 1],
            Column.ROAD_TYPE.value: [RoadType.GRAVEL, RoadType.HIGH_WAY, RoadType.RESIDENTIAL,
                                     RoadType.HIGH_WAY, RoadType.RESIDENTIAL, RoadType.HIGH_WAY,
                                     RoadType.HIGH_WAY, RoadType.RESIDENTIAL, RoadType.HIGH_WAY,
                                     RoadType.HIGH_WAY]
        }
        self.data_df = pd.DataFrame(self.data)

        self.records = [
            AnalysisRecord(
                _required_data=(
                    SettingRecord(
                        _identifier="",

                        _context=HistogramAnalysis().setting_name,
                        _selection=SelectionRecord(
                            selected=[Column.SPEED.value],
                            option=DiscreteOption(Column.val_list())
                        )
                    ),
                )
            ),
            AnalysisRecord(
                _required_data=(
                    SettingRecord(
                        _identifier="",

                        _context=HistogramAnalysis().setting_name,
                        _selection=SelectionRecord(
                            selected=[Column.ACCELERATION.value],
                            option=DiscreteOption(Column.val_list())
                        )
                    ),
                )
            ),
            AnalysisRecord(
                _required_data=(
                    SettingRecord(
                        _identifier="",

                        _context=HistogramAnalysis().setting_name,
                        _selection=SelectionRecord(
                            selected=[Column.ROAD_TYPE.value],
                            option=DiscreteOption(Column.val_list())
                        )
                    ),
                )
            )]
        # Speed
        self.results: [pd.DataFrame] = [pd.DataFrame({Column.SPEED.value: [50, 40, 10, 20, 30, 52, 100],
                                                      'Occurrence': [3, 2, 1, 1, 1, 1, 1]}),

                                        # Acceleration
                                        pd.DataFrame({Column.ACCELERATION.value: [1, 2, 3, 4],
                                                      'Occurrence': [4, 3, 2, 1]}),
                                        # RoadType
                                        pd.DataFrame({Column.ROAD_TYPE.value: [RoadType.HIGH_WAY,
                                                                               RoadType.RESIDENTIAL, RoadType.GRAVEL],
                                                      'Occurrence': [6, 3, 1]})
                                        ]

    def test_get_required_columns(self):
        """
        Assert the analysis requires one data of the database.
        """
        required_columns = self.analysis.get_required_columns()
        self.assertEqual(len(required_columns), len(Column.list()))
        # self.analysis.set_analysis_parameters()
        self.assertIsInstance(Column.get_column_from_str(required_columns[0]), Column)

    def test_get_name(self):
        """
        Asserts that the _name of the analysis is 'histogram analysis'
        """
        name = self.analysis.get_name()
        self.assertEqual(name, "histogram")

    def test_get_required_analysis_parameter(self):
        """
        Asserts that the required choices for the analysis are a choice of columns from which one is chosen by default.
        """
        required_parameters = self.analysis.get_required_analysis_parameter()
        self.assertEqual(len(required_parameters.required_data), 1)
        self.assertEqual(len(required_parameters.required_data[0].selection.selected), 1)
        self.assertIsInstance(Column.get_column_from_str(required_parameters.required_data[0].selection.selected[0]),
                              Column)
        self.assertListEqual(required_parameters.required_data[0].selection.option.get_option(), Column.val_list())

    def test_set_analysis_parameters(self):
        """
        Tests that the parameters of the analysis can be set.
        """
        record = AnalysisRecord(
            _required_data=(
                SettingRecord(
                    _identifier="",

                    _context=HistogramAnalysis().setting_name,
                    _selection=SelectionRecord(
                        selected=[Column.ACCELERATION.value],
                        option=DiscreteOption(Column.val_list())
                    )
                ),
            )
        )
        self.analysis.set_analysis_parameters(record)
        required_columns = self.analysis.get_required_columns()
        self.assertEqual(required_columns, [Column.ACCELERATION.value])

    def test_set_invalid_analysis_parameters(self):
        """
        Checks that invalid parameters of the analysis cannot be set.
        """
        invalid_cases = [
            # record does not contain the correct amount of option
            AnalysisRecord(
                _required_data=(
                    SettingRecord(
                        _identifier="",

                        _context="parameters",
                        _selection=SelectionRecord(
                            selected=[Column.SPEED.value],
                            option=DiscreteOption(Column.val_list())
                        )
                    ),
                    SettingRecord(
                        _identifier="",

                        _context="parameters",
                        _selection=SelectionRecord(
                            selected=[Column.ACCELERATION.value],
                            option=DiscreteOption(Column.val_list())
                        )
                    )
                )
            ),
            # no parameter was selected in the record
            AnalysisRecord(
                _required_data=(
                    SettingRecord(
                        _identifier="",

                        _context="parameters",
                        _selection=SelectionRecord(
                            selected=[],
                            option=DiscreteOption(Column.val_list()),
                            possible_selection_range=range(0, 1)
                        )
                    ),
                )
            ),
            # Multiple columns selected
            AnalysisRecord(
                _required_data=(
                    SettingRecord(
                        _identifier="",

                        _context=HistogramAnalysis().setting_name,
                        _selection=SelectionRecord(
                            selected=[Column.SPEED.value, Column.ACCELERATION.value],
                            option=DiscreteOption(Column.val_list()),
                            possible_selection_range=range(1, 3)
                        )
                    ),
                )
            ),
        ]
        for i, invalid_record in enumerate(invalid_cases):
            with self.subTest(i=i):
                self.assertRaises(InvalidInput, self.analysis.set_analysis_parameters, invalid_record)

    def test_analyse(self):
        """
        Tests that the analysis analyses the data correctly by comparing the result with the expected results.
        In addition, it also checks if the DataRecord was created correctly.
        """
        data_record = DataRecord("Test Data", tuple(self.data.keys()), self.data_df)
        for i, record in enumerate(self.records):
            self.analysis.set_analysis_parameters(record)
            result = self.analysis.analyse(data_record.data)
            # self.assertEqual(result.data._name, f"histogram of data "
            # f"{record.required_data[0].selection.selected[0]}")
            self.assertEqual(result.data.column_names[0], record.required_data[0].selection.selected[0])
            self.assertEqual(len(result.data.column_names), 2)
            self.assertEqual(result.id.value, AnalysisViewEnum.histogram_view.value)
            self.assertTrue(result.data.data.equals(self.results[i]))


if __name__ == '__main__':
    unittest.main()
