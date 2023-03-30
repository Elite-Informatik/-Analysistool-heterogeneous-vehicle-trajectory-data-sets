import unittest

import pandas as pd

from src.data_transfer.content import Column
from src.data_transfer.exception import InvalidInput
from src.data_transfer.record import AnalysisRecord
from src.data_transfer.record.selection_record import SelectionRecord
from src.data_transfer.record.setting_record import SettingRecord
from src.data_transfer.selection.discrete_option import DiscreteOption
from src.model.analysis_structure.concrete_analysis.plot_analysis import PlotAnalysis


class TestPlotAnalysis(unittest.TestCase):

    def test_get_required_analysis_parameter(self):
        """
        Test if the get_required_analysis_parameter method returns the expected result of AnalysisRecord instance.
        It also checks if the analysis excepts its own record.
        """
        plot_analysis = PlotAnalysis()
        parameters = plot_analysis.get_required_analysis_parameter()
        self.assertIsInstance(parameters, AnalysisRecord)
        self.assertTrue(plot_analysis.set_analysis_parameters(parameters))

    def test_set_analysis_parameters(self):
        """
        Test if the set_analysis_parameters method sets the analysis parameters correctly and returns True.
        """
        plot_analysis = PlotAnalysis()
        record = AnalysisRecord(
            _required_data=(
                SettingRecord(
                    _identifier="",

                    _context=PlotAnalysis()._x_attribute,
                    _selection=SelectionRecord(
                        selected=[Column.TIME.value],
                        option=DiscreteOption(Column.val_list())
                    )
                ),
                SettingRecord(
                    _identifier="",

                    _context=PlotAnalysis()._y_attribute,
                    _selection=SelectionRecord(
                        selected=[Column.SPEED.value],
                        option=DiscreteOption(Column.val_list())
                    )
                ),
            )
        )
        self.assertTrue(plot_analysis.set_analysis_parameters(record))
        self.assertListEqual(plot_analysis.get_required_columns(), [Column.TIME.value, Column.SPEED.value])

    def test_set_analysis_parameters_with_incorrect_record(self):
        """
        Test if the set_analysis_parameters method raises a ValueError when the input AnalysisRecord is incorrect.
        """
        plot_analysis = PlotAnalysis()
        record = AnalysisRecord(
            _required_data=(
                SettingRecord(
                    _identifier="",
                    _context="x_axis_attribute",
                    _selection=SelectionRecord(
                        selected=[Column.TIME],
                        option=DiscreteOption(Column.list())
                    )
                ),
            )
        )
        with self.assertRaises(InvalidInput):
            plot_analysis.set_analysis_parameters(record)

    def test_plot_analysis_analyse(self):
        """
        Test if the analyse method returns the expected DataRecord instance with the correct data.
        """
        record = AnalysisRecord(
            _required_data=(
                SettingRecord(
                    _identifier="",

                    _context=PlotAnalysis()._x_attribute,
                    _selection=SelectionRecord(
                        selected=[Column.TIME.value],
                        option=DiscreteOption(Column.val_list())
                    )
                ),
                SettingRecord(
                    _identifier="",

                    _context=PlotAnalysis()._y_attribute,
                    _selection=SelectionRecord(
                        selected=[Column.SPEED.value],
                        option=DiscreteOption(Column.val_list())
                    )
                ),
            )
        )
        plot_analysis = PlotAnalysis()
        plot_analysis.set_analysis_parameters(record)
        data = pd.DataFrame(
            {Column.ID.value: [1, 2, 3, 3, 3], Column.TIME.value: [1, 2, 3, 4, 5],
             Column.SPEED.value: [2, 20, 35, 50, 52]})
        result = plot_analysis.analyse(data=data)
        self.assertEqual(result.data._name, PlotAnalysis()._name)
        self.assertTupleEqual(result.data.column_names, (Column.TIME.value, Column.SPEED.value))
        del data[Column.ID.value]
        self.assertEqual(data.to_dict(), result.data.data.to_dict())


if __name__ == '__main__':
    unittest.main()
