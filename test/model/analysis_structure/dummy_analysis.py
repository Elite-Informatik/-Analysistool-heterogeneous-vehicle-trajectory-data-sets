from src.data_transfer.content import Column
from src.data_transfer.record import AnalysisDataRecord
from src.data_transfer.record import AnalysisRecord
from src.data_transfer.record import DataRecord
from src.data_transfer.record.selection_record import SelectionRecord
from src.data_transfer.record.setting_record import SettingRecord
from src.data_transfer.selection.interval_value_option import IntervalValueOption
from src.model.analysis_structure.Analysis import Analysis


class DummyAnalysis(Analysis):

    def set_analysis_parameters(self, parameters: AnalysisRecord) -> bool:
        pass

    Analysis_view_id: str = "Test_view"

    def get_name(self) -> str:
        return "Dummy Analysis"

    analysis_record: AnalysisRecord \
        = AnalysisRecord((SettingRecord("test_setting", SelectionRecord([5], IntervalValueOption(1, 10)), ""),))

    def __init__(self):
        self.parameters = None
        super().__init__()
        self._required_parameters = [Column.ID]

    def analyse(self, data: DataRecord) -> AnalysisDataRecord:
        return AnalysisDataRecord(data, self.get_name())

    def get_required_analysis_parameter(self) -> AnalysisRecord:
        return self.analysis_record


CONSTRUCTOR = DummyAnalysis
