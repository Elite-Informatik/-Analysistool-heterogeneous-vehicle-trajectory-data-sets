from pandas import DataFrame

from src.file.file.exporter.data_exporter import DataExporter


class FeatherExporter(DataExporter):
    """
    Class representing a FeatherExporter.
    """

    def get_file_format(self) -> str:
        return 'feather'

    def export_data(self, path: str, data: DataFrame):
        data.to_feather(path)
