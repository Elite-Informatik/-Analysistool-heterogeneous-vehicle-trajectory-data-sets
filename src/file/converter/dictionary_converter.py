from typing import List

import pandas as pd
from pandas import DataFrame

from src.data_transfer.record.data_record import DataRecord
from src.file.converter.converter import Converter


class DictionaryConverter(Converter):
    """
    converts data records to dictionary and back
    """

    def __init__(self):
        pass

    def is_convertable(self, data: DataFrame) -> bool:
        """
        checks whether the data frame can be converted to a dictionary.
        :param data:    the dataframe
        :return:        whether the data can be converted to dict
        """
        # You can check by overwriting if each data record has certain attributes,
        # that are necessary to convert it to dictionary
        # and return True if all are present, otherwise False.
        if data is None:
            return False
        return True

    def search_inaccuracies(self, data: List[DataRecord]) -> List[str]:
        """
        searches for inaccuracies in the given data records
        :param data:    list of data records
        :return:        list of inaccuracies
        """
        inaccuracies = []
        # You can iterate through the data records and check for certain conditions
        # that may indicate inaccuracies in the data.
        for record in data:
            if len(record.name) > 100:
                inaccuracies.append(f"Name field in record {record} exceeds maximum length of 100")
        return inaccuracies

    def get_standart_file_names(self) -> List[str]:
        """
        This method returns a list of standard file names.
        """
        return list()

    def convert_to_dictionary(self, data: DataFrame) -> dict:
        """
        converts data frame to the corresponding dictionary representation of the data
        :param data:    the data frame
        :return:        the dictionary
        """
        # You can use python's built-in `vars()` function to return the __dict__ attribute of the object
        data = data.to_dict(orient='split')
        dictionary = {}
        if len(data['data']) == 0 and 'data' in data:
            return dictionary
        for column, data in zip(data['columns'], data['data'][0]):
            dictionary[column] = data
        return dictionary

    def convert_to_data(self, dictionary: dict) -> DataFrame:
        """
        converts dictionary to its corresponding DataRecord object representation of the dictionary
        :param dictionary:  the dictionary
        :return:            the data frame
        """
        # You can use the python's built-in `type` function to create a new object of a certain class
        return pd.DataFrame(dictionary, index=[0])
