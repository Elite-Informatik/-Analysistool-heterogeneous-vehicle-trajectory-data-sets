import os
from unittest import skip

from src.data_transfer.content import Column
from src.data_transfer.record import AnalysisDataRecord
from src.model.analysis_structure.concrete_analysis.heatmap_analysis import HeatmapAnalysis
from test.integration.pseudo_monkey.analyses.fcd_ui_analysis_controller_test import FcdUIAnalysisControllerTest
from test.integration.pseudo_monkey.analyses.fcd_ui_analysis_controller_test import set_record_selected

slow_mode = int(os.environ.get("SLOW_MODE", 1))  # get the value of slow mode from the environment variable or use 0


# as default


class HeatMapTest(FcdUIAnalysisControllerTest):

    def setUp(self) -> None:

        self.name = HeatmapAnalysis()._name
        super().setUp()
        self.init_analysis(self.name)

    def test_set_heatmap(self):
        """
        Tests that the heatmap analysis can be set with all combinations of x, y and color axis.
        """

        for x_axis in Column:
            for y_axis in Column:
                for color_axis in Column:
                    if x_axis == y_axis or x_axis == color_axis or y_axis == color_axis:
                        continue
                    with self.subTest(msg="x_axis: " + x_axis.name + " y_axis: " + y_axis.name
                                          + " color_axis: " + color_axis.name):
                        analysis_record = set_record_selected(self.analysis_settings, [x_axis, y_axis, color_axis])
                        self.controller.communication_facade.change_analysis(analysis_id=self.analysis_id,
                                                                             new_analysis_settings=analysis_record)
                        data_record: AnalysisDataRecord = self.controller.data_request_facade.get_analysis_data(
                            analysis_id=self.analysis_id)
                        self.assertIsNotNone(data_record.data, "data is None for " + x_axis.name + " " + y_axis.name)
                        self.assertNotEqual(data_record.data.data.shape[0], 0, "x axis is empty for " + x_axis.name)
                        self.assertNotEqual(data_record.data.data.shape[1], 0, "y axis is empty for " + y_axis.name)

