import unittest
from typing import List

from src.data_transfer.content import Column
from src.data_transfer.record import AnalysisRecord
from src.data_transfer.record import SettingRecord
from src.model.analysis_structure.concrete_analysis.heatmap_analysis import HeatmapAnalysis
from test.integration.test_open_fcdui_dataset import OpenFCDUIDatasetControllerTest


def set_record_selected(settings: AnalysisRecord, columns: List[Column]):
    """
    A helper function to set the selected columns in the analysis settings.
    :param settings: the analysis settings as AnalysisRecord
    :param columns: the columns to set as selected
    :return: a new AnalysisRecord with the selected columns
    """
    new_settings = []
    for i, column in enumerate(columns):
        new_settings.append(SettingRecord(_context=settings.required_data[i].context,
                                          _selection=settings.required_data[0].selection
                                          .set_selected([column.value])))
    return AnalysisRecord(_required_data=tuple(new_settings))


class FcdUIAnalysisControllerTest(OpenFCDUIDatasetControllerTest):

    def setUp(self) -> None:
        """
        Sets up a generic analysis controller test. This test is a subtype of the OpenFCDUIDatasetControllerTest.
        """
        super().setUp()

    def init_analysis(self, name: str = HeatmapAnalysis()._name):
        """
        Initializes the analysis with the given name and sets attributes for the subclasses.
        :param name: the name of the analysis
        """
        analyses = self.controller.data_request_facade.get_analysis_types()
        analysis_type = [analysis for analysis in analyses if analysis.name == name][0]
        self.controller.communication_facade.add_analysis(analysis_type)
        self.analysis_id = self.events.pop().id
        self.analysis_settings: AnalysisRecord = \
            self.controller.data_request_facade.get_analysis_settings(uuid=self.analysis_id)


if __name__ == '__main__':
    unittest.main()
