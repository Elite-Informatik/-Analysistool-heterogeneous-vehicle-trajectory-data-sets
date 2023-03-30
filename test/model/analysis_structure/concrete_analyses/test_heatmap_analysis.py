import unittest

import pandas as pd

from src.data_transfer.content import Column
from src.data_transfer.exception import InvalidInput
from src.data_transfer.record import AnalysisDataRecord
from src.data_transfer.record import AnalysisRecord
from src.data_transfer.record.selection_record import SelectionRecord
from src.data_transfer.record.setting_record import SettingRecord
from src.data_transfer.selection.discrete_option import DiscreteOption
from src.model.analysis_structure.concrete_analysis.heatmap_analysis import HeatmapAnalysis


class TestHeatmapAnalysis(unittest.TestCase):

    def test_get_required_analysis_parameter(self):
        heatmap_analysis = HeatmapAnalysis()
        self.assertIsInstance(heatmap_analysis.get_required_analysis_parameter(), AnalysisRecord)

    def test_set_analysis_parameters(self):
        heatmap_analysis = HeatmapAnalysis()
        record = AnalysisRecord(
            _required_data=(
                SettingRecord(
                    _identifier="",

                    _context="x axis attribute",
                    _selection=SelectionRecord(
                        selected=[Column.ID.value],
                        option=DiscreteOption(Column.val_list())
                    )
                ),
                SettingRecord(
                    _identifier="",

                    _context="y axis attribute",
                    _selection=SelectionRecord(
                        selected=[Column.TIME.value],
                        option=DiscreteOption(Column.val_list())
                    )
                ),
                SettingRecord(
                    _identifier="",

                    _context="color attribute",
                    _selection=SelectionRecord(
                        selected=[Column.SPEED.value],
                        option=DiscreteOption(Column.val_list())
                    )
                ),
            )
        )
        self.assertTrue(heatmap_analysis.set_analysis_parameters(record))
        # self.assertEqual(Analysis.get_columns_from_setting(setting_name=heatmap_analysis._x_attribute)[0], Column.ID)
        # self.assertEqual(heatmap_analysis._y_attribute, Column.TIME)
        # self.assertEqual(heatmap_analysis._color_attribute, Column.SPEED)
        self.assertListEqual(heatmap_analysis.get_required_columns(), [Column.ID.value, Column.TIME.value,
                                                                       Column.SPEED.value])

    def test_set_analysis_parameters_with_incorrect_record(self):
        heatmap_analysis = HeatmapAnalysis()
        record = AnalysisRecord(
            _required_data=(
                SettingRecord(
                    _identifier="",

                    _context="x_axis_attribute",
                    _selection=SelectionRecord(
                        selected=[Column.ID],
                        option=DiscreteOption(Column.list())
                    )
                ),
            )
        )
        with self.assertRaises(InvalidInput) as error:
            heatmap_analysis.set_analysis_parameters(record)

    def test_heatmap_analysis_analyse(self):
        record = AnalysisRecord(
            _required_data=(
                SettingRecord(
                    _identifier="",

                    _context="x axis attribute",
                    _selection=SelectionRecord(
                        selected=[Column.ID.value],
                        option=DiscreteOption(Column.val_list())
                    )
                ),
                SettingRecord(
                    _identifier="",

                    _context="y axis attribute",
                    _selection=SelectionRecord(
                        selected=[Column.TIME.value],
                        option=DiscreteOption(Column.val_list())
                    )
                ),
                SettingRecord(
                    _identifier="",

                    _context="color attribute",
                    _selection=SelectionRecord(
                        selected=[Column.SPEED.value],
                        option=DiscreteOption(Column.val_list())
                    )
                ),
            )
        )
        heatmap_analysis = HeatmapAnalysis()
        heatmap_analysis.set_analysis_parameters(record)
        data = pd.DataFrame({
            Column.ID.value: [1, 2, 3, 4, 5] * 5,
            Column.TIME.value: [1] * 5 + [2] * 5 + [3] * 5 + [4] * 5 + [5] * 5,
            Column.SPEED.value: [1] * 5 + [2] * 5 + [3] * 5 + [4] * 5 + [5] * 5,
            Column.SPEED_LIMIT.value: [50, 50, 50, 50, 50] * 5
        })
        result: AnalysisDataRecord = heatmap_analysis.analyse(data)

        expected_result: pd.DataFrame = pd.DataFrame({1: {1: 1, 2: 2, 3: 3, 4: 4, 5: 5},
                                                      2: {1: 1, 2: 2, 3: 3, 4: 4, 5: 5},
                                                      3: {1: 1, 2: 2, 3: 3, 4: 4, 5: 5},
                                                      4: {1: 1, 2: 2, 3: 3, 4: 4, 5: 5},
                                                      5: {1: 1, 2: 2, 3: 3, 4: 4, 5: 5}}
                                                     )

        self.assertDictEqual(expected_result.to_dict(), result.data.data.to_dict())
