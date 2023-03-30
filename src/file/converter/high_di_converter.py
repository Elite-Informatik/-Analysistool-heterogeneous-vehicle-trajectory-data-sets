from enum import Enum
from re import match
from typing import List
from typing import Union

from pandas import DataFrame

from src.data_transfer.record import DataRecord
from src.file.converter.data_converter import DataConverter
from src.file.converter.highd_handler.concrete_highd_handler import RecordingMetaHandler

SEP: str = ","


class SubFileTypes(Enum):
    """
    holds all names of the subfiles of the high di dataset
    """

    RECORDING_META = "recordingMeta"
    TRACKS_META = "tracksMeta"
    TRACKS = "tracks"


PREFIX: str = r"\d*_"
FORMAT: str = "HighD"
DEF_NAME: str = "HighD Dataset"
INVALID_FILES_ERROR = "Error, invalid files"


class HighDIConverter(DataConverter):
    """
    this converter converts a dataset in the high di into the unified dataformat
    """

    def __init__(self):
        self._handler = RecordingMetaHandler()

    def convert_to_data(self, data: List[DataRecord]) -> Union[DataRecord, None]:
        if data is None:
            return None

        if not files_valid(data):
            return None

        DataRecord(DEF_NAME, tuple(), DataFrame())

        recording_meta = get_file(data, SubFileTypes.RECORDING_META.value)
        tracks_meta = get_file(data, SubFileTypes.TRACKS_META.value)
        tracks = get_file(data, SubFileTypes.TRACKS.value)
        final_data = DataRecord(DEF_NAME, tuple(), DataFrame())

        self._handler.repair(recording_meta, tracks_meta, tracks, final_data)
        imported_data = self._handler.import_column(recording_meta, tracks_meta, tracks, final_data)
        return imported_data

    def get_data_format(self) -> str:
        return FORMAT

    def is_convertable(self, data: List[DataRecord]) -> bool:
        if data is None:
            return False

        if not files_valid(data):
            return False

        recording_meta = get_file(data, SubFileTypes.RECORDING_META.value)
        tracks_meta = get_file(data, SubFileTypes.TRACKS_META.value)
        tracks = get_file(data, SubFileTypes.TRACKS.value)
        final_data = DataRecord(DEF_NAME, tuple(), DataFrame())

        fatal_corrupts = self._handler.list_fatal_corrupts(recording_meta=recording_meta, track_meta=tracks_meta,
                                                           tracks=tracks, final_data=final_data)
        for entry in fatal_corrupts:
            if entry:
                return False

        return True

    def search_inaccuracies(self, data: List[DataRecord]) -> List[str]:
        if not files_valid(data):
            return [INVALID_FILES_ERROR]

        recording_meta = get_file(data, SubFileTypes.RECORDING_META.value)
        tracks_meta = get_file(data, SubFileTypes.TRACKS_META.value)
        tracks = get_file(data, SubFileTypes.TRACKS.value)
        final_data = DataRecord(DEF_NAME, tuple(), DataFrame())

        results = self._handler.list_reparable_corrupts(recording_meta, tracks_meta, tracks, final_data)
        message: List[str] = []
        for corrupt_type in results.keys():
            if not results[corrupt_type]:
                continue
            header: str = corrupt_type.value + ": "
            for concrete_corrupt in results[corrupt_type]:
                header += str(concrete_corrupt) + ", "
            header = header[:-2]
            message.append(header)
        return message

    def get_separator(self) -> str:
        return SEP


def get_file(data: List[DataRecord], file: str) -> Union[DataRecord, None]:
    """
    gets the data record of the corresponding file
    :param data:    the list of datarecord
    :param file:    the searched file name
    :return:        the corresponding data record
    """
    pattern = PREFIX + file + r"$"
    for record in data:
        if match(pattern, record.name):
            return record
    return None


def files_valid(data: List[DataRecord]) -> bool:
    """
    checks whether the list of data records are valid (that they contain every subfile)
    :param data:    the list of data records
    :return:        whether they are valid
    """
    for file_type in [e.value for e in SubFileTypes]:
        if get_file(data, file_type) is None:
            return False
    return True
