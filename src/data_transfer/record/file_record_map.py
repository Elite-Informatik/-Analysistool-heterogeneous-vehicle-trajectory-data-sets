import os

from PIL.Image import Image

from src.data_transfer.record import FileRecord


class FileRecordMap(FileRecord):
    """
    represents a png file
    """

    def __init__(self, image: Image, name: str):
        self._file_name: str = name
        self._image: Image = image

    def save(self, path: str):
        self._image.save(os.path.join(path, self._file_name + ".png"))
