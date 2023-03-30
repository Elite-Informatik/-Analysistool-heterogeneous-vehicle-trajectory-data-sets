from src.data_transfer.record import PolygonRecord
from src.data_transfer.record import PositionRecord
from test.integration.test_open_fcdui_dataset import OpenFCDUIDatasetControllerTest


class AnalysisTest(OpenFCDUIDatasetControllerTest):

    def test_add_analysis_path_time(self):
        analyses = self.controller.data_request_facade.get_analysis_types()
        path_time_analysis = [analysis for analysis in analyses if analysis.name == "path time"][0]
        poly_start = PolygonRecord(_name="polystart", _corners=(
            PositionRecord(_longitude=50.0591001, _latitude=8.6130358),
            PositionRecord(_longitude=50.0594683, _latitude=8.6324336),
            PositionRecord(_longitude=50.0491079, _latitude=8.6319186),
            PositionRecord(_longitude=50.0486119, _latitude=8.6114909)
        ))
        poly_end = PolygonRecord(_name="polyend", _corners=(
            PositionRecord(_longitude=50.0674085, _latitude=8.7061456),
            PositionRecord(_longitude=50.0682900, _latitude=8.7178186),
            PositionRecord(_longitude=50.0579315, _latitude=8.7194494),
            PositionRecord(_longitude=50.0561130, _latitude=8.7070898)
        ))
        self.controller.communication_facade.add_polygon(polygon=poly_start)
        self.controller.communication_facade.add_polygon(polygon=poly_end)
        self.controller.communication_facade.add_analysis(path_time_analysis)
        analysis_id = self.events.pop().id
        data_record = self.controller.data_request_facade.get_analysis_data(analysis_id)
        self.assertIsNotNone(data_record)
