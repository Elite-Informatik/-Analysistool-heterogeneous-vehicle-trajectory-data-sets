from typing import List

import pandas as pd

from src.data_transfer.content.column import Column
from src.data_transfer.record import DataRecord
from src.file.converter.data_converter import DataConverter

DEF_VAL = None


class InternConverter(DataConverter):
    """
    converts a dataset in the unified dataformat into the unified dataformat (does nothing)
    """

    def convert_to_data(self, data: List[DataRecord]) -> DataRecord:
        data = data.pop()
        for column in Column:
            if column.value not in data.data:
                data.data[column.value] = DEF_VAL

        data.data[Column.ORDER.value] = data.data.reset_index()["index"]
        # set the time column to type TIME.
        #data.data[Column.TIME.value] = pd.to_datetime(data.data[Column.TIME.value], format="%H:%M:%S")
        return data

    def get_data_format(self) -> str:
        return "intern"

    def is_convertable(self, data: List[DataRecord]) -> bool:
        return True

    def search_inaccuracies(self, data: List[DataRecord]) -> List[str]:
        return []
