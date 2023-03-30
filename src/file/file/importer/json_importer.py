from pandas import read_json

from src.data_transfer.record import DataRecord
from src.file.file.importer.data_importer import DataImporter


class JSONImporter(DataImporter):
    """
    Class representing a JSONImporter.
    """

    def fits_file_format(self, name: str) -> bool:
        return name.endswith('.json')

    def import_data(self, path: str, sep: str = "") -> DataRecord:
        data = read_json(path, orient='records')
        return DataRecord(path, data.columns, data)

    @property
    def file_format(self) -> str:
        return r'^.*\.json$'
