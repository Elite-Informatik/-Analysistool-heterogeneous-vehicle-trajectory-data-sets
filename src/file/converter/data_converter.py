from abc import abstractmethod
from typing import List

from src.data_transfer.record.data_record import DataRecord
from src.file.converter.converter import Converter


class DataConverter(Converter):
    """
    this abstract class converts a dataset of a certain format into the unified dataformat
    """

    @abstractmethod
    def convert_to_data(self, data: List[DataRecord]) -> DataRecord:
        """
        converts a dataset of a certain format into the unified dataformat
        :param data:    the dataset
        :return:        the dataset in the unified dataformat
        """
        pass

    @abstractmethod
    def get_data_format(self) -> str:
        """
        the name of the specific dataformat
        """
        pass
