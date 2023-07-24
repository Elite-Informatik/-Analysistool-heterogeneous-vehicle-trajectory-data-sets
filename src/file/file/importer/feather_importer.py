from pandas import read_feather

from src.data_transfer.record import DataRecord
from src.file.file.importer.data_importer import DataImporter


class FeatherImporter(DataImporter):
    """
    Class representing a FeatherImporter.
    """

    def yield_import_data(self, path: str, sep: str = ",") -> DataRecord:
        raise NotImplemented("Not implemented!")

    def fits_file_format(self, name: str) -> str:
        return name.endswith('.feather')

    def import_data(self, path: str, sep: str = "") -> DataRecord:
        data = read_feather(path)
        return DataRecord(_column_names=data.columns, _data=data, _name=path)

    @property
    def file_format(self) -> str:
        return r'^.*\.feather$'
