import unittest
from unittest import skip

from src.model.analysis_structure.concrete_analysis.plot_analysis import PlotAnalysis
from src.data_transfer.record import AnalysisDataRecord
from test.integration.pseudo_monkey.analyses.fcd_ui_analysis_controller_test import set_record_selected, \
    FcdUIAnalysisControllerTest
from src.data_transfer.content import Column
from src.data_transfer.record import AnalysisRecord, AnalysisDataRecord


class PlotTest(FcdUIAnalysisControllerTest):

    def setUp(self) -> None:
        #self.name = "plot"
        super().setUp()
        self.init_analysis(PlotAnalysis()._name)
        self.assertEqual(PlotAnalysis()._name,
                         self.controller.data_request_facade.get_analysis_data(self.analysis_id).data.name)

    @skip("Not implemented")
    def test_set_plot(self):
        """
        Tests that the plot analysis can be set with all combinations of x, y
        """
        for x_axis in Column:
            for y_axis in Column:
                with self.subTest(msg="x_axis: " + x_axis.name + " y_axis: " + y_axis.name):
                    analysis_record = set_record_selected(self.analysis_settings, [x_axis, y_axis])
                    self.controller.communication_facade.change_analysis(analysis_id=self.analysis_id,
                                                                         new_analysis_settings=analysis_record)
                    self.events.pop()
                    data_record: AnalysisDataRecord = self.controller.data_request_facade.get_analysis_data(
                        analysis_id=self.analysis_id)

                    self.assertIsNotNone(data_record.data, "data is None for " + x_axis.name + " " + y_axis.name)
                    self.assertNotEqual(data_record.data.data.shape[0], 0, "x axis is empty for " + x_axis.name)
                    self.assertNotEqual(data_record.data.data.shape[1], 0, "y axis is empty for " + y_axis.name)


if __name__ == '__main__':
    unittest.main()
