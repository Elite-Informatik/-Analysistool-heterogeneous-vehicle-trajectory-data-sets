import os

from matplotlib.figure import Figure

from src.data_transfer.record import FileRecord


class FileRecordSvg(FileRecord):
    """
    represents a svg file
    """

    def __init__(self, figure: Figure, name: str):
        self._file_name: str = name
        self._figure: Figure = figure

    def save(self, path: str):
        self._figure.savefig(os.path.join(path, self._file_name + ".svg"))
