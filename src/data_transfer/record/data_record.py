from dataclasses import dataclass
from typing import Tuple

from pandas import pandas


@dataclass(frozen=True)
class DataRecord:
    """
    record used to transfer dataframes
    """

    _name: str
    _column_names: Tuple
    _data: pandas.DataFrame

    @property
    def name(self):
        """
        the name of the dataframe
        """
        return self._name

    @property
    def column_names(self):
        """
        the columns
        """
        return self._column_names

    @property
    def data(self):
        """
        the dataframe containing the data
        """
        return self._data
