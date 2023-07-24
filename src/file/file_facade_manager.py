from typing import Callable
from typing import Dict
from typing import List
from typing import Optional

from src.data_transfer.record.data_record import DataRecord
from src.data_transfer.record.file_record import FileRecord
from src.file.converter.data_converter import DataConverter
from src.file.converter.dictionary_converter import DictionaryConverter
from src.file.converter.fcd_ui_converter import FCDUIConverter
from src.file.converter.high_di_converter import HighDIConverter
from src.file.converter.intern_converter import InternConverter
from src.file.converter.simra_bicycle_converter import SimraConverter
from src.file.file.file_structure import FileStructure
from src.file.file_facade import FileFacade
from src.model.error_handler import ErrorMessage


class FileFacadeManager(FileFacade):
    """
    The FileManager implements the file model_manager interface. It uses the UserInput and the File facade
    to structure the file program flow.
    """

    PATH_NOT_FOUND_MESSAGE: str = "The standard path of the program does not exist in the file system"
    DATA_CONVERTES: List = [InternConverter, HighDIConverter, FCDUIConverter, SimraConverter]

    _analysis_standard_path: str
    _dictionary_standart_path: str
    _data_converters: Dict[str, DataConverter]

    def __init__(self):
        super().__init__()
        self.session_open = False
        self.separator = None
        self.converter = None
        self.data = list()
        self._file_structure: FileStructure = None
        self._dictionary_converter: DictionaryConverter = DictionaryConverter()
        self._data_converters = {}
        for data_converter in self.DATA_CONVERTES:
            self._data_converters[data_converter().get_data_format()] = data_converter()
        self.set_file_structure(FileStructure())
        self._analysis_standard_path = None
        self._dictionary_standart_path = None

    def set_standard_paths(self, analysis_standart_path: str, dictionary_standart_path: str) -> bool:

        analysis_standart_path = self._file_structure.concatinate_standart_path(analysis_standart_path)
        dictionary_standart_path = self._file_structure.concatinate_standart_path(dictionary_standart_path)

        if self._file_structure.exists_path(analysis_standart_path):
            self._file_structure.create_path(analysis_standart_path)

        if self._file_structure.exists_path(dictionary_standart_path):
            self._file_structure.create_path(dictionary_standart_path)

        if not self._file_structure.exists_path(dictionary_standart_path):
            self.throw_error(ErrorMessage.DICT_PATH_NOT_EXISTING)
            return False
        self._dictionary_standart_path = dictionary_standart_path

        if not self._file_structure.exists_path(analysis_standart_path):
            self.throw_error(ErrorMessage.ANALYSIS_PATH_NOT_EXISTING)
            return False
        self._analysis_standard_path = analysis_standart_path
        return True

    def export_data_file(self, path: str, data: DataRecord, file_format: str) -> bool:
        data_exported: bool = self._file_structure.export_data(path, data.name, data.data, file_format)
        if not data_exported:
            self.throw_error(ErrorMessage.EXPORT_ERROR)
            return False
        return True

    def open_session(self, allways_imported, file_format) -> None:
        if self.session_open:
            raise Exception("Session is already open")
        self.converter = self._data_converters[file_format]
        self.separator = self.converter.get_separator()
        self.session_open = True
        self.converter.open_session()

        for path in allways_imported:
            self.data.append(self._file_structure.import_file(path, self.separator))

    def import_data_files(self, chucked_path: str, inaccuracies: List[str]) -> Optional[DataRecord]:
        if not self.session_open:
            raise Exception("Session is not open")

        for chunk in self._file_structure.yield_import_data(chucked_path, self.separator):
            if not self.converter.is_convertable(self.data + [chunk]):
                self.throw_error(ErrorMessage.DATASET_NOT_IMPORTABLE)
                yield None

            inaccuracies.extend(self.converter.search_inaccuracies(self.data + [chunk]))
            converted_data = self.converter.convert_to_data(self.data + [chunk])
            yield converted_data

    def close_session(self):
        if not self.session_open:
            raise Exception("Session is not open")

        self.session_open = False
        self.converter.close_session()

    def export_file(self, path: str, file: FileRecord) -> bool:
        return self._file_structure.export_file(path, file)

    def export_dictionary_to_standard_path(self, name: str, dictionary: dict):

        data = self._dictionary_converter.convert_to_data(dictionary)

        return self._file_structure.export_data(self._dictionary_standart_path, name, data, "json")

    def import_dictionary_from_standard_path(self, name: str) -> Optional[Dict]:
        data_record = self._file_structure.import_data_by_name(self._dictionary_standart_path, name)
        if data_record is None:
            self.throw_error(ErrorMessage.IMPORT_ERROR)
            return None
        if not (self._dictionary_converter.is_convertable(data_record.data)):
            self.throw_error(ErrorMessage.DICT_NOT_IMPORTABLE)
            return None
        return self._dictionary_converter.convert_to_dictionary(data_record.data)

    def get_analysis_types_from_standard_path(self) -> List[Callable[[], object]]:

        modules = list()
        # Die module werden importiert
        for path in self._file_structure.search_path(self._analysis_standard_path, r".*\.py"):
            modules.append(self._file_structure.import_python_module(path))
        # Die jedes modul wird in einen constructor umgewandelt
        constructors = list()
        for modul in modules:
            constructors.append(modul.CONSTRUCTOR)

        return constructors

    def import_new_analysis_to_standard_path(self, from_path: str) -> bool:
        self._file_structure.move_file(from_path, self._analysis_standard_path)
        return True

    def set_file_structure(self, file_facade: FileStructure):
        self._file_structure = file_facade

    @property
    def exportable_file_formats(self) -> List[str]:

        return self._file_structure.exportable_file_formats

    @property
    def convertabele_file_formats(self) -> List[str]:

        return list(self._data_converters.keys())
