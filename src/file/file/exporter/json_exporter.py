from pandas import DataFrame

from src.file.file.exporter.data_exporter import DataExporter


class JSONExporter(DataExporter):
    """
    Class representing a JSONExporter.
    """

    def get_file_format(self) -> str:
        return 'json'

    def export_data(self, path: str, data: DataFrame):
        data.to_json(path, orient='records')
