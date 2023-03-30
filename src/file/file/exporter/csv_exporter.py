from pandas import DataFrame

from src.file.file.exporter.data_exporter import DataExporter


class CSVExporter(DataExporter):
    """
    Class representing a CSVExporter.
    """

    def get_file_format(self) -> str:
        return 'csv'

    def export_data(self, path: str, data: DataFrame):
        data.to_csv(path, index=False)
