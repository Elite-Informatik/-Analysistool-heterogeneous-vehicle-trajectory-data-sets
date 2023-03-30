import unittest

import pandas as pd

from src.data_transfer.content import Column
from src.data_transfer.exception import InvalidInput
from src.data_transfer.record import AnalysisRecord
from src.data_transfer.record import DataRecord
from src.data_transfer.record.selection_record import SelectionRecord
from src.data_transfer.record.setting_record import SettingRecord
from src.data_transfer.selection.discrete_option import DiscreteOption
from src.model.analysis_structure.concrete_analysis.transmission_analysis import TransmissionFrequencyAnalysis


class TestTransmissionAnalysis(unittest.TestCase):
    def setUp(self) -> None:
        self.analysis = TransmissionFrequencyAnalysis()
        id1 = 1
        id3 = 3
        df = pd.DataFrame({Column.TRAJECTORY_ID.value: [id1, id1, id1, id3, id3, id3, id3],
                           Column.DATE.value: ["01.01.2020", "01.01.2020", "01.01.2020", "01.01.2020", "01.01.2020",
                                               "01.01.2020",
                                               "01.01.2020"],
                           Column.TIME.value: ["08:00:00", "08:00:02", "08:00:03", "08:00:00", "08:01:00", "08:02:00",
                                               "08:03:00", ]})
        self.data_record = DataRecord("data", df.columns, df)

        self.average = pd.DataFrame({Column.TRAJECTORY_ID.value: [id1, id3],
                                     'time_diff': [1.5, 60.0]})
        self.distribution = pd.DataFrame({'time_diff': [60.0, 2.0, 1.0],
                                          'Occurrence': [3, 1, 1]})

        self._average_record: AnalysisRecord = AnalysisRecord(
            _required_data=(
                SettingRecord(
                    _identifier="",
                    _context=TransmissionFrequencyAnalysis().setting_name,
                    _selection=SelectionRecord(
                        selected=['average'],
                        option=DiscreteOption(['average', 'distribution'])
                    )
                ),
            )
        )
        self._distribution_record: AnalysisRecord = AnalysisRecord(
            _required_data=(
                SettingRecord(
                    _identifier="",
                    _context=TransmissionFrequencyAnalysis().setting_name,
                    _selection=SelectionRecord(
                        selected=['distribution'],
                        option=DiscreteOption(['average', 'distribution'])
                    )
                ),
            )
        )

    def test_get_required_columns(self) -> None:
        expected_columns = [Column.TRAJECTORY_ID.value, Column.DATE.value, Column.TIME.value]
        self.assertListEqual(self.analysis.get_required_columns(), expected_columns)

    def test_get_required_analysis_parameter(self) -> None:
        expected_record = AnalysisRecord(
            _required_data=(
                SettingRecord(
                    _identifier="",
                    _context=TransmissionFrequencyAnalysis().setting_name,
                    _selection=SelectionRecord(
                        selected=["average"],
                        option=DiscreteOption(["average", "distribution"])
                    )
                ),
            )
        )
        self.assertListEqual(self.analysis.get_required_analysis_parameter().required_data[0].selection.selected
                             , expected_record.required_data[0].selection.selected)

    def test_get_name(self) -> None:
        self.assertEqual(self.analysis.get_name(), "transmission")

    def test_set_analysis_parameters(self) -> None:
        record = AnalysisRecord(
            _required_data=(
                SettingRecord(
                    _identifier="",
                    _context=TransmissionFrequencyAnalysis().setting_name,
                    _selection=SelectionRecord(
                        selected=["distribution"],
                        option=DiscreteOption(["average", "distribution"])
                    )
                ),
            )
        )
        self.assertTrue(self.analysis.set_analysis_parameters(record))
        self.assertEqual(self.analysis.get_setting_selected(TransmissionFrequencyAnalysis().setting_name),
                         ["distribution"])

    def test_set_analysis_parameters_invalid_record(self) -> None:
        record = AnalysisRecord(
            _required_data=(
                SettingRecord(
                    _identifier="",
                    _context="analysis_type",
                    _selection=SelectionRecord(
                        selected=["average", "distribution"],
                        option=DiscreteOption(["average", "distribution"]),
                        possible_selection_range=range(1, 3)
                    )
                ),
            )
        )
        self.assertRaises(InvalidInput, self.analysis.set_analysis_parameters, record)

    def test_average(self):
        self.analysis.set_analysis_parameters(self._average_record)
        result = self.analysis.analyse(self.data_record.data)
        self.assertDictEqual(result.data.data.to_dict(), self.average.to_dict())

    def test_distribution(self):
        self.analysis.set_analysis_parameters(self._distribution_record)
        result = self.analysis.analyse(self.data_record.data)
        self.assertDictEqual(result.data.data.to_dict(), self.distribution.to_dict())


if __name__ == '__main__':
    unittest.main()
