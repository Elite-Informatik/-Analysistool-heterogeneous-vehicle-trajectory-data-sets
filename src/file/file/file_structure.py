import importlib
import os
import re
import shutil
from typing import Dict
from typing import List

from pandas import DataFrame

from src.data_transfer.record import DataRecord
from src.data_transfer.record import FileRecord
from src.file.file.exporter.csv_exporter import CSVExporter
from src.file.file.exporter.data_exporter import DataExporter
from src.file.file.exporter.feather_exporter import FeatherExporter
from src.file.file.exporter.json_exporter import JSONExporter
from src.file.file.importer.csv_importer import CSVImporter
from src.file.file.importer.data_importer import DataImporter
from src.file.file.importer.feather_importer import FeatherImporter
from src.file.file.importer.json_importer import JSONImporter
from src.file.file.unpacker.gz_unpacker import GZUnpacker
from src.file.file.unpacker.unpacker import Unpacker
from src.file.file.unpacker.zip_unpacker import ZipUnpacker

DataImporters: List = [CSVImporter, FeatherImporter, JSONImporter]
DataExporters: List = [CSVExporter, FeatherExporter, JSONExporter]
DataUnpackers: List = [GZUnpacker, ZipUnpacker]

STANDARD_SEP: str = ","


class FileStructure:
    """
    represents a file structure responsible for managing files
    """

    _data_unpackers: List[Unpacker]
    _data_importers: List[DataImporter]
    _data_exporter: Dict[str, DataExporter]

    def __init__(self):
        self._data_unpackers = []
        for data_unpacker in DataUnpackers:
            self._data_unpackers.append(data_unpacker())

        self._data_importers = []
        for data_importer in DataImporters:
            self._data_importers.append(data_importer())

        self._data_exporters = {}
        for data_exporter in DataExporters:
            self._data_exporters[data_exporter().get_file_format()] = data_exporter()

    @property
    def exportable_file_formats(self) -> List[str]:
        """
        gets a list of all exportable file formats
        :return:    all exportable file formats
        """
        return list(self._data_exporters.keys())

    def create_path(self, path: str) -> bool:
        """
        Creates the given path in the os file system
        :param path: THe path to create
        """
        if self.exists_path(path):
            return False
        os.makedirs(path)
        return True

    def exists_path(self, path: str) -> bool:
        """
        checks whether the path is a valid directory
        :param path:    the path
        :return:        whether path is valid directory
        """
        return os.path.isdir(path)

    def exists_file(self, path: str) -> bool:
        """
        checks whether the path is a valid file
        :param path:    the path
        :return:        whether the path is a valid file
        """
        return os.path.isfile(path)

    def concatinate_standart_path(self, path: str) -> str:
        """
        concatenates the working directory with the path
        :param path:    the path
        :return:        the concatenated path
        """
        return os.path.join(os.getcwd(), path)

    def move_file(self, source_file: str, destination: str):
        """
        moves the file to the destination path
        :param source_file: the file to move
        :param destination: the destination path
        """
        return shutil.copy(source_file, destination)

    def export_data(self, path: str, name: str, data: DataFrame, file_format: str) -> bool:
        """
        exports the data in the given format at the given path
        :param path:        the path
        :param name:        the name
        :param data:        the data
        :param file_format: the file format
        :return:            whether export was successful
        """
        path = os.path.join(path, name + "." + file_format)
        self._data_exporters[file_format].export_data(path, data)
        return True

    def export_file(self, path: str, file: FileRecord) -> bool:
        """
        exports the given file at the given path
        :param path:    the path
        :param file:    the file to export
        :return:        whether the export was successful
        """
        file.save(path)
        return True

    def import_python_module(self, path: str) -> object:
        """
        imports a python module at the given path
        :param path:    the path of the module
        :return:        the module
        """
        spec = importlib.util.spec_from_file_location("module", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def search_path(self, path: str, file_format: str) -> List[str]:
        """
        gets all paths of the files in the given format at the given path
        :param path:        the path
        :param file_format: the file format
        :return:            the
        """
        files = []

        for root, dirs, filenames in os.walk(path):
            dirs[:] = []  # clear the list of directories to search in to avoid recursion
            for file in filenames:
                if re.search(file_format, file):
                    files.append(os.path.join(root, file))
        return files

    def import_data(self, path: str) -> List[DataRecord]:
        """
        Imports dataframes from the path and returns it in datarecords
        """
        for unpacker in self._data_unpackers:
            if unpacker.fits_file_format(path):
                path = unpacker.unpack(path)

        if self.exists_file(path):
            return [self.import_file(path)]

        if self.exists_path(path):
            for importer in self._data_importers:
                paths: List[str] = self.search_path(path, importer.file_format)
                if len(paths) > 0:
                    return [importer.import_data(path) for path in paths]

    def import_data_by_name(self, path: str, name: str):
        """
        Imports datafiles based on the file name
        """
        for file in os.listdir(path):
            if file.startswith(name):
                return self.import_file(os.path.join(path, file))

    def import_file(self, path: str, sep: str = STANDARD_SEP):
        """
        Imports file with a given separator
        """
        for importer in self._data_importers:
            if importer.fits_file_format(path):
                return importer.import_data(path, sep)

    def yield_import_data(self, path: str, sep: str = STANDARD_SEP):
        """
        Yields data from a given path
        """
        for importer in self._data_importers:
            if importer.fits_file_format(path):
                yield from importer.yield_import_data(path, sep)
