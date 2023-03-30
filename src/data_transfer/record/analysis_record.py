from dataclasses import dataclass
from typing import Tuple

from src.data_transfer.record.setting_record import SettingRecord


@dataclass(frozen=True)
class AnalysisRecord:
    """
    record that holds the settings of an analysis
    """

    _required_data: Tuple[SettingRecord, ...]

    @property
    def required_data(self):
        """
        the required settings
        """
        return self._required_data
