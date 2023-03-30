import re
from abc import ABC
from abc import abstractmethod
from collections import defaultdict
from enum import Enum
from math import floor
from re import split
from typing import Dict
from typing import List
from typing import Union
from uuid import UUID
from uuid import uuid4

import numpy as numpy
import pandas as pd

from src.data_transfer.content import Column
from src.data_transfer.content.road_type import RoadType
from src.data_transfer.record import DataRecord
from src.file.converter.util.data_util import add_distance_to_latitude
from src.file.converter.util.data_util import add_distance_to_longitude
from src.file.converter.util.data_util import calculate_drection
from src.file.converter.util.data_util import find_duplicate_rows
from src.file.converter.util.data_util import find_non_date_rows
from src.file.converter.util.data_util import find_non_matching_rows
from src.file.converter.util.data_util import find_non_numeric_rows
from src.file.converter.util.data_util import repair_date_column
from src.file.converter.util.data_util import repair_number_column
from src.file.converter.util.data_util import repair_string_column
from src.file.converter.util.data_util import print_non_date_rows
from src.file.converter.util.data_util import print_non_numeric_rows
from src.file.converter.util.data_util import print_duplicate_rows
from src.file.converter.util.data_util import print_non_matching_rows

DEF_SEARCH_SIZE: float = 100
DEF_ROAD_TYPE: RoadType = RoadType.MOTORWAY
DEF_DAY: str = "01."
DEF_ROAD_ID: int = 0
DEF_POINT_ID: int = -1
DEF_FRAME_ID = -1
DEF_TIME: str = "00:00"
DEF_SPEED_LIMIT: int = 420
DEF_DATE: numpy.datetime64 = numpy.datetime64("0000-01-01")
DEF_LAT_LOC: float = 0
DEF_X_LOC: float = 0
DEF_Y_LOC: int = 0
DEF_X_SPEED: int = 0
DEF_Y_SPEED: int = 0
DEF_X_SPEED_DIR: int = 0
DEF_Y_SPEED_DIR: int = 0
DEF_X_ACC: int = 0
DEF_Y_ACC: int = 0
DEF_X_ACC_DIR: int = 0
DEF_Y_ACC_DIR: int = 0

DEF_VAL = None
SPEED_MULT: float = 3.6

HEAD_OFFSET: float = 180
FRAME: str = "frame"
TRACK: str = "track"
TIME_SPLIT: str = ":"
HOUR_TO_SEC: int = 3600
MIN_TO_SEC: int = 60
TIME_REGEX: re.Pattern = re.compile(r"\d\d:\d\d")
LAT = "Lat"
LONG = "Long"
HEAD = "Head"
LOCATION_IDS: Dict[int, Dict[str, float]] = {1: {LAT: 50.853999, LONG: 6.550469, HEAD: 30},
                                             2: {LAT: 51.408919, LONG: 6.426914, HEAD: 5},
                                             3: {LAT: 51.408919, LONG: 6.426914, HEAD: 5},
                                             4: {LAT: 50.853999, LONG: 6.550469, HEAD: 30},
                                             5: {LAT: 50.853999, LONG: 6.550469, HEAD: 30},
                                             6: {LAT: 51.408919, LONG: 6.426914, HEAD: 5}}


class MetaColumn(Enum):
    """
    holds all columns of the metadata
    """

    ID = "id"
    FRAME_RATE = "frameRate"
    LOCATION_ID = "locationId"
    SPEED_LIMIT = "speedLimit"
    MONTH = "month"
    WEEK_DAY = "weekDay"
    START_TIME = "startTime"
    DURATION = "duration"
    TOTAL_DRIVEN_DISTANCE = "totalDrivenTime"
    NUM_VEHICLES = "numVehicles"
    NUM_CARS = "numCars"
    NUM_TRUCKS = "numTrucks"
    UPPER_LANE_MARKINGS = "upperLaneMarkings"
    LOWER_LANE_MARKINGS = "lowerLaneMarkings"

    FRAME = "frame"
    INITIAL_FRAME = "initialFrame"
    X_POSITION = "x"
    Y_POSITION = "y"
    X_VELOCITY = "xVelocity"
    Y_VELOCITY = "yVelocity"
    X_ACCELERATION = "xAcceleration"
    Y_ACCELERATION = "yAcceleration"


class ReparableCorrupts(Enum):
    """
    holds all kinds of repairable corruptions
    """

    DUPLICATES = "Duplicates"
    INVALID_NUMBER = "Invalid Number"
    INVALID_STRING = "Invalid String"
    INVALID_DATE = "Invalid Date"


class FatalCorrupts(Enum):
    """
    holds all kinds of fatal corruptions
    """

    REQUIRED_ROW_MISSING = "Required row missing"


def gen_uuid() -> UUID:
    """
    generates a new uuid
    :return: a new UUID
    """
    return uuid4()


def sec_to_time(sec: float) -> str:
    """
    converts seconds to time
    :param sec:     number seconds
    :return:         the time in string format
    """
    hours: int = floor(sec / 3600)
    mins: int = floor((sec % 3600) / 60)
    secs: int = floor(sec - 3600 * hours - 60 * mins)
    return str(hours) + ":" + str(mins) + ":" + str(secs)


class RecordingMetaHandler:
    """
    this handler is responsible for the recording metadata
    """

    REQUIRED_COLUMNS: List[MetaColumn] = [MetaColumn.ID.value, MetaColumn.MONTH.value, MetaColumn.WEEK_DAY.value,
                                          MetaColumn.START_TIME.value]

    def __init__(self):
        self._column_handler: List[ColumnHandler] = [IDHandler(), Time(), SpeedLimit(), Date(), Location(), Speed(),
                                                     Acceleration(), SpeedDirection(), AccelerationDirection(),
                                                     Road(), RoadId(), OneWay(), Filtered()]

    def import_column(self, recording_meta: DataRecord, track_meta: DataRecord, tracks: DataRecord,
                      final_data: DataRecord) -> Union[DataRecord, None]:
        """
        This method copies a specific column to the final dataframe. It is possible to determine the values
        indirectly through other columns values.
        """

        column_list: List[Column] = []
        for handler in self._column_handler:
            added_columns: List[Column] = handler.get_valid_column()
            column_list.extend(added_columns)

        new_data: DataRecord = DataRecord(final_data.name, tuple(column_list), final_data.data)

        for handler in self._column_handler:
            if not handler.import_column(recording_meta, track_meta, tracks, new_data):
                return None

        for column in Column:
            if column.value not in new_data.data:
                new_data.data[column.value] = DEF_VAL

        new_data.data[Column.ORDER.value] = new_data.data.reset_index()["index"]
        return new_data

    def repair(self, recording_meta: DataRecord, track_meta: DataRecord, tracks: DataRecord,
               final_data: DataRecord) -> bool:
        """
        repairs the repairable corruptions
        :param recording_meta:  the recording metadata
        :param track_meta:      the track metadata
        :param tracks:          the tracks data
        :param final_data:      the destination data
        :return:                whether the repairing was successful
        """
        assert (isinstance(recording_meta, DataRecord))
        assert (isinstance(track_meta, DataRecord))
        assert (isinstance(tracks, DataRecord))
        assert (isinstance(final_data, DataRecord))

        for handler in self._column_handler:
            if not handler.repair(recording_meta, track_meta, tracks, final_data):
                return False

        return True

    def list_reparable_corrupts(self, recording_meta: DataRecord, track_meta: DataRecord, tracks: DataRecord,
                                final_data: DataRecord) -> Dict[ReparableCorrupts, List]:
        """
        This method checks for a specific column if it's correctly formatted to be transferred. Otherwise,
        it returns a map with faults and the rows where the fault happened.
        :param recording_meta:  the recording metadata
        :param track_meta:      the track metadata
        :param tracks:          the tracks data
        :param final_data:      the destination data
        :return:                the repairable corruptions
        """

        corrupted_dict: Dict[ReparableCorrupts, List] = {}

        for handler in self._column_handler:
            result = handler.get_repairable_corrupts(recording_meta, track_meta,
                                                     tracks, final_data)

            for key, value in result.items():
                if key in corrupted_dict:
                    corrupted_dict[key].extend(value)
                else:
                    corrupted_dict[key] = value

        return corrupted_dict

    def list_fatal_corrupts(self, recording_meta: DataRecord, track_meta: DataRecord, tracks: DataRecord,
                            final_data: DataRecord) -> Dict[FatalCorrupts, List]:
        """
        This method checks for a specific column if it's correctly formatted to be transferred. Otherwise,
        it returns a map with faults and the rows where the fault happened.
        :param recording_meta:  the recording metadata
        :param track_meta:      the track metadata
        :param tracks:          the tracks data
        :param final_data:      the destination data
        :return:                the fatal corruptions
        """

        corrupted_dict: Dict[FatalCorrupts, List] = {}

        for handler in self._column_handler:
            result = handler.get_fatal_corrupts(recording_meta, track_meta,
                                                tracks, final_data)

            for key, value in result.items():
                if key in corrupted_dict:
                    corrupted_dict[key].extend(value)
                else:
                    corrupted_dict[key] = value

        return corrupted_dict


class ColumnHandler(ABC):
    """
    For each row, there exists a column handler which provides specific functionality to determine both correctness
    and consistency.
    """

    def __init__(self):
        """
        Constructor for a ColumnHandler
        """
        self.last_fatal_checked: pd.DataFrame = None
        self.last_repairable_checked: pd.DataFrame = None
        self.last_repaired: pd.DataFrame = None

    @abstractmethod
    def get_valid_column(self) -> List[Column]:
        pass

    def import_column(self, recording_meta: DataRecord, track_meta: DataRecord, tracks: DataRecord,
                      final_data: DataRecord) -> bool:
        """
        This method copies a specific column to the final dataframe. It is possible to determine the values
        indirectly through other columns values.
        :param recording_meta:  the recording metadata
        :param track_meta:      the track metadata
        :param tracks:          the tracks data
        :param final_data:      the destination data
        :return:                whether the import was successful
        """
        assert (isinstance(recording_meta, DataRecord))
        assert (isinstance(track_meta, DataRecord))
        assert (isinstance(tracks, DataRecord))
        assert (isinstance(final_data, DataRecord))

        self.transfer_column(recording_meta, track_meta, tracks, final_data)
        return True

    def transfer_column(self, recording_meta: DataRecord, track_meta: DataRecord, tracks: DataRecord,
                        final_data: DataRecord):
        """
        transfers the column into the final dataframe
        :param recording_meta:  the recording metadata
        :param track_meta:      the track metadata
        :param tracks:          the tracks data
        :param final_data:      the destination data
        """
        pass

    def repair(self, recording_meta: DataRecord, track_meta: DataRecord, tracks: DataRecord,
               final_data: DataRecord) -> bool:
        """
        repairs the column
        :param recording_meta:  the recording metadata
        :param track_meta:      the track metadata
        :param tracks:          the tracks data
        :param final_data:      the destination data
        :return:                whether the repairing was successful
        """
        assert (isinstance(recording_meta, DataRecord))
        assert (isinstance(track_meta, DataRecord))
        assert (isinstance(tracks, DataRecord))
        assert (isinstance(final_data, DataRecord))

        self.concrete_repair(recording_meta, track_meta, tracks, final_data)
        return True

    def concrete_repair(self, recording_meta: DataRecord, track_meta: DataRecord, tracks: DataRecord,
                        final_data: DataRecord) -> bool:
        """
        repairs the concrete column
        :param recording_meta:  the recording metadata
        :param track_meta:      the track metadata
        :param tracks:          the tracks data
        :param final_data:      the destination data
        :return:                whether the repairing was successful
        """
        pass

    def get_fatal_corrupts(self, recording_meta: DataRecord, track_meta: DataRecord, tracks: DataRecord,
                           final_data: DataRecord) -> Dict[FatalCorrupts, List]:
        """
        This method searches for fatal corrupts in the column
        :param recording_meta:  the recording metadata
        :param track_meta:      the track metadata
        :param tracks:          the tracks data
        :param final_data:      the destination data
        :return:                the fatal corruptions
        """
        assert (isinstance(recording_meta, DataRecord))
        assert (isinstance(track_meta, DataRecord))
        assert (isinstance(tracks, DataRecord))
        assert (isinstance(final_data, DataRecord))

        return self.get_concrete_fatal_corrupts(recording_meta, track_meta, tracks, final_data)

    def get_concrete_fatal_corrupts(self, recording_meta: DataRecord, track_meta: DataRecord, tracks: DataRecord,
                                    final_data: DataRecord) -> Dict[FatalCorrupts, List]:
        """
        This method searches for fatal corrupts in the concrete column
        :param recording_meta:  the recording metadata
        :param track_meta:      the track metadata
        :param tracks:          the tracks data
        :param final_data:      the destination data
        :return:                the fatal corruptions
        """
        pass

    def get_repairable_corrupts(self, recording_meta: DataRecord, track_meta: DataRecord, tracks: DataRecord,
                                final_data: DataRecord) -> Dict[ReparableCorrupts, List]:
        """
        This method searches for repairable corrupts in the column
        :param recording_meta:  the recording metadata
        :param track_meta:      the track metadata
        :param tracks:          the tracks data
        :param final_data:      the destination data
        :return:                the repairable corruptions
        """
        assert (isinstance(recording_meta, DataRecord))
        assert (isinstance(track_meta, DataRecord))
        assert (isinstance(tracks, DataRecord))
        assert (isinstance(final_data, DataRecord))

        return self.get_concrete_repairable_corrupts(recording_meta, track_meta, tracks, final_data)

    def get_concrete_repairable_corrupts(self, recording_meta: DataRecord, track_meta: DataRecord, tracks: DataRecord,
                                         final_data: DataRecord) -> Dict[ReparableCorrupts, List]:
        """
        This method checks for a specific column if it's correctly formatted to be transferred. Otherwise,
        it returns a map with faults and the rows where the fault happened.
        :param recording_meta:  the recording metadata
        :param track_meta:      the track metadata
        :param tracks:          the tracks data
        :param final_data:      the destination data
        :return:                the repairable corruptions
        """
        pass


class IDHandler(ColumnHandler):
    """
    this handler is responsible for the datapoint IDs and the trajectory IDs
    """

    def get_valid_column(self) -> List[Column]:
        valid_column = [Column.ID, Column.TRAJECTORY_ID]
        return valid_column

    def transfer_column(self, recording_meta: DataRecord, track_meta: DataRecord, tracks: DataRecord,
                        final_data: DataRecord):

        # create individual uuids
        tracks.data[Column.ID] = pd.DataFrame([gen_uuid() for _ in range(tracks.data.shape[0])])
        # create trajectory uuids
        track_meta.data[Column.ID] = pd.DataFrame([gen_uuid() for _ in range(track_meta.data.shape[0])])

        # Create map from track ids to track uuids
        map_data_frame: pd.DataFrame = track_meta.data[[MetaColumn.ID.value,
                                                        Column.ID]]
        id_to_start_map = map_data_frame.set_index(MetaColumn.ID.value).T.to_dict("records")[0]

        # Apply map to the track frame
        tracks.data[Column.TRAJECTORY_ID] = tracks.data[MetaColumn.ID.value].map(id_to_start_map)

        # Transfer columns from source dataframes to final dataframe
        final_data.data[Column.ID.value] = tracks.data[Column.ID]
        final_data.data[Column.TRAJECTORY_ID.value] = tracks.data[Column.TRAJECTORY_ID]

        # Drop temporary columns
        tracks.data.drop(Column.ID, axis=1)
        tracks.data.drop(Column.TRAJECTORY_ID, axis=1)

    def get_concrete_fatal_corrupts(self, recording_meta: DataRecord, track_meta: DataRecord, tracks: DataRecord,
                                    final_data: DataRecord) -> Dict[FatalCorrupts, List]:

        corrupted_dict: Dict[FatalCorrupts, List] = defaultdict(list)

        if MetaColumn.FRAME.value not in tracks.data:
            corrupted_dict[FatalCorrupts.REQUIRED_ROW_MISSING].append(MetaColumn.FRAME)
        if MetaColumn.ID.value not in tracks.data:
            corrupted_dict[FatalCorrupts.REQUIRED_ROW_MISSING].append(MetaColumn.ID)
        if MetaColumn.ID.value not in track_meta.data:
            corrupted_dict[FatalCorrupts.REQUIRED_ROW_MISSING].append(MetaColumn.ID)
        if MetaColumn.ID.value not in recording_meta.data:
            corrupted_dict[FatalCorrupts.REQUIRED_ROW_MISSING].append(MetaColumn.ID)

        return corrupted_dict

    def get_concrete_repairable_corrupts(self, recording_meta: DataRecord, track_meta: DataRecord, tracks: DataRecord,
                                         final_data: DataRecord) -> Dict[ReparableCorrupts, List]:
        corrupted_dict: Dict[ReparableCorrupts, List] = defaultdict(list)

        datapoint_column: pd.DataFrame = tracks.data[MetaColumn.FRAME.value]
        trajectory_column: pd.DataFrame = tracks.data[MetaColumn.ID.value]
        id_column: pd.DataFrame = pd.DataFrame()
        id_column[MetaColumn.ID.value] = track_meta.data[MetaColumn.ID.value]

        corrupted_dict[ReparableCorrupts.INVALID_NUMBER].extend(print_non_numeric_rows(datapoint_column))
        corrupted_dict[ReparableCorrupts.INVALID_NUMBER].extend(print_non_numeric_rows(trajectory_column))
        corrupted_dict[ReparableCorrupts.INVALID_NUMBER].extend(print_non_numeric_rows(id_column[MetaColumn.ID.value]))

        duplicate_rows = print_duplicate_rows(id_column, id_column.columns)
        if len(duplicate_rows) == 0:
            return corrupted_dict

        duplicate_message = ["Columns" + track_meta.name + ", " + MetaColumn.ID.value + " " + duplicate_rows[0]]
        corrupted_dict[ReparableCorrupts.DUPLICATES].extend(duplicate_message)
        return corrupted_dict

    def concrete_repair(self, recording_meta: DataRecord, track_meta: DataRecord, tracks: DataRecord,
                        final_data: DataRecord) -> bool:

        datapoint_column: pd.DataFrame = tracks.data[MetaColumn.FRAME.value]
        trajectory_column: pd.DataFrame = tracks.data[MetaColumn.ID.value]
        id_column: pd.DataFrame = track_meta.data[MetaColumn.ID.value]

        tracks.data[MetaColumn.FRAME.value] = repair_number_column(datapoint_column, DEF_FRAME_ID)
        tracks.data[MetaColumn.ID.value] = repair_number_column(trajectory_column, DEF_POINT_ID)
        track_meta.data[MetaColumn.ID.value] = repair_number_column(id_column, DEF_POINT_ID)

        return True


class Time(ColumnHandler):
    """
    this handler is responsible for the time
    """

    def get_valid_column(self) -> List[Column]:
        return [Column.TIME]

    def transfer_column(self, recording_meta: DataRecord, track_meta: DataRecord, tracks: DataRecord,
                        final_data: DataRecord):
        frame_length: float = 1 / recording_meta.data[MetaColumn.FRAME_RATE.value][0]

        # Get time in seconds
        string_time: List[str] = split(TIME_SPLIT, recording_meta.data[MetaColumn.START_TIME.value][0])
        start_time: int = int(string_time[0]) * HOUR_TO_SEC
        start_time += int(string_time[1]) * MIN_TO_SEC

        map_data_frame: pd.DataFrame = track_meta.data[[MetaColumn.ID.value,
                                                        MetaColumn.INITIAL_FRAME.value]]
        id_to_start_map = map_data_frame.set_index(MetaColumn.ID.value).T.to_dict("records")[0]
        tracks.data["initialTime"] = tracks.data[MetaColumn.ID.value].map(id_to_start_map)
        tracks.data["total_time"] = \
            tracks.data["initialTime"].astype(float) + tracks.data[MetaColumn.FRAME.value].astype(float)
        tracks.data["total_time"] = tracks.data["total_time"].mul(frame_length)
        tracks.data["total_time"] += start_time
        final_data.data[Column.TIME.value] = pd.to_datetime(tracks.data["total_time"].apply(sec_to_time),
                                                            format="%H" + TIME_SPLIT + "%M" + TIME_SPLIT + "%S")
        tracks.data.drop("total_time", axis=1)
        tracks.data.drop("initialTime", axis=1)

    def get_concrete_fatal_corrupts(self, recording_meta: DataRecord, track_meta: DataRecord, tracks: DataRecord,
                                    final_data: DataRecord) -> Dict[FatalCorrupts, List]:

        corrupted_dict: Dict[FatalCorrupts, List] = defaultdict(list)

        if MetaColumn.START_TIME.value not in recording_meta.data:
            corrupted_dict[FatalCorrupts.REQUIRED_ROW_MISSING].append(MetaColumn.START_TIME)
        if MetaColumn.ID.value not in track_meta.data:
            corrupted_dict[FatalCorrupts.REQUIRED_ROW_MISSING].append(MetaColumn.ID)
        if MetaColumn.INITIAL_FRAME.value not in track_meta.data:
            corrupted_dict[FatalCorrupts.REQUIRED_ROW_MISSING].append(MetaColumn.INITIAL_FRAME)
        if MetaColumn.FRAME.value not in tracks.data:
            corrupted_dict[FatalCorrupts.REQUIRED_ROW_MISSING].append(MetaColumn.FRAME)
        if MetaColumn.ID.value not in tracks.data:
            corrupted_dict[FatalCorrupts.REQUIRED_ROW_MISSING].append(MetaColumn.ID)

        return corrupted_dict

    def get_concrete_repairable_corrupts(self, recording_meta: DataRecord, track_meta: DataRecord, tracks: DataRecord,
                                         final_data: DataRecord) -> Dict[ReparableCorrupts, List]:

        corrupted_dict: Dict[ReparableCorrupts, List] = defaultdict(list)

        frame_column: pd.DataFrame = track_meta.data[MetaColumn.INITIAL_FRAME.value]
        start_time_column: pd.DataFrame = recording_meta.data[MetaColumn.START_TIME.value]

        corrupted_dict[ReparableCorrupts.INVALID_NUMBER].extend(print_non_numeric_rows(frame_column))
        corrupted_dict[ReparableCorrupts.INVALID_NUMBER].extend(print_non_matching_rows(start_time_column, TIME_REGEX))

        return corrupted_dict

    def concrete_repair(self, recording_meta: DataRecord, track_meta: DataRecord, tracks: DataRecord,
                        final_data: DataRecord) -> bool:

        frame_column: pd.DataFrame = pd.DataFrame(track_meta.data[MetaColumn.INITIAL_FRAME.value])
        start_time_column: pd.DataFrame = pd.DataFrame(recording_meta.data[MetaColumn.START_TIME.value])

        track_meta.data[MetaColumn.INITIAL_FRAME.value] = repair_number_column(frame_column, DEF_FRAME_ID)
        recording_meta.data[MetaColumn.START_TIME.value] = repair_string_column(start_time_column, def_value=DEF_TIME)

        return True


class SpeedLimit(ColumnHandler):
    """
    this column handler is responsible for the speed limit
    """

    def get_valid_column(self) -> List[Column]:
        return [Column.SPEED_LIMIT]

    def transfer_column(self, recording_meta: DataRecord, track_meta: DataRecord, tracks: DataRecord,
                        final_data: DataRecord):
        # Take speed limit of first row. Stands for every track since the tracks stays the same
        # Creates a second dataframe with one column speed_limit and every entry has got the same speed limit entry.
        # Thereafter, it is integrated in the final data_frame
        final_data.data[Column.SPEED_LIMIT.value] = recording_meta.data[MetaColumn.SPEED_LIMIT.value][0] * SPEED_MULT

    def get_concrete_fatal_corrupts(self, recording_meta: DataRecord, track_meta: DataRecord, tracks: DataRecord,
                                    final_data: DataRecord) -> Dict[FatalCorrupts, List]:
        corrupted_dict: Dict[FatalCorrupts, List] = defaultdict(list)

        if MetaColumn.SPEED_LIMIT.value not in recording_meta.data:
            corrupted_dict[FatalCorrupts.REQUIRED_ROW_MISSING].append(MetaColumn.SPEED_LIMIT)
            return corrupted_dict

        return corrupted_dict

    def get_concrete_repairable_corrupts(self, recording_meta: DataRecord, track_meta: DataRecord, tracks: DataRecord,
                                         final_data: DataRecord) -> Dict[ReparableCorrupts, List]:
        corrupted_dict: Dict[ReparableCorrupts, List] = defaultdict(list)

        speed_limit_column: pd.DataFrame = recording_meta.data[MetaColumn.SPEED_LIMIT.value]

        corrupted_dict[ReparableCorrupts.INVALID_NUMBER].extend(print_non_numeric_rows(speed_limit_column))

        return corrupted_dict

    def concrete_repair(self, recording_meta: DataRecord, track_meta: DataRecord, tracks: DataRecord,
                        final_data: DataRecord) -> bool:
        speed_limit_column: pd.DataFrame = recording_meta.data[MetaColumn.SPEED_LIMIT.value]

        recording_meta.data[MetaColumn.SPEED_LIMIT.value] = repair_number_column(speed_limit_column, DEF_SPEED_LIMIT)

        return True


class Date(ColumnHandler):
    """
    this column handler is responsible for the date
    """

    def get_valid_column(self) -> List[Column]:
        return [Column.DATE]

    def transfer_column(self, recording_meta: DataRecord, track_meta: DataRecord, tracks: DataRecord,
                        final_data: DataRecord):
        date = format_date(str(recording_meta.data[MetaColumn.MONTH.value][0]))
        final_data.data[Column.DATE.value] = numpy.datetime64(date[2] + "-" + date[1] + "-" + date[0])

    def get_concrete_fatal_corrupts(self, recording_meta: DataRecord, track_meta: DataRecord, tracks: DataRecord,
                                    final_data: DataRecord) -> Dict[FatalCorrupts, List]:
        corrupted_dict: Dict[FatalCorrupts, List] = defaultdict(list)

        if MetaColumn.MONTH.value not in recording_meta.data:
            corrupted_dict[FatalCorrupts.REQUIRED_ROW_MISSING].append(MetaColumn.MONTH)
            return corrupted_dict

        return corrupted_dict

    def get_concrete_repairable_corrupts(self, recording_meta: DataRecord, track_meta: DataRecord, tracks: DataRecord,
                                         final_data: DataRecord) -> Dict[ReparableCorrupts, List]:
        corrupted_dict: Dict[ReparableCorrupts, List] = defaultdict(list)

        corrupted_dict[ReparableCorrupts.INVALID_NUMBER].extend(
            print_non_date_rows(recording_meta.data[MetaColumn.MONTH.value]))

        return corrupted_dict

    def concrete_repair(self, recording_meta: DataRecord, track_meta: DataRecord, tracks: DataRecord,
                        final_data: DataRecord) -> bool:
        date_column: pd.DataFrame = recording_meta.data[MetaColumn.MONTH.value]

        track_meta.data[MetaColumn.MONTH.value] = repair_date_column(date_column, DEF_DATE)

        return True


class Location(ColumnHandler):
    """
    this column handler is responsible for latitude and longitude
    """

    def get_valid_column(self) -> List[Column]:
        return [Column.LATITUDE, Column.LONGITUDE]

    def transfer_column(self, recording_meta: DataRecord, track_meta: DataRecord, tracks: DataRecord,
                        final_data: DataRecord):
        location_id: Dict[str, float] = LOCATION_IDS[recording_meta.data[MetaColumn.LOCATION_ID.value][0]]
        lat: float = location_id[LAT]
        long: float = location_id[LONG]
        head: float = location_id[HEAD]

        # Adds a distance vector including x and y distance and a heading onto coordinates.
        # Performed in a pandas dataframe with lambda expressions applying the respective function
        # The lambda function uses the existing x and y position columns to calculate the global coordinates.
        final_data.data[Column.LATITUDE.value] = tracks.data.apply(
            lambda row: add_distance_to_latitude(lat, row[MetaColumn.X_POSITION.value],
                                                 row[MetaColumn.Y_POSITION.value], head), axis=1)

        final_data.data[Column.LONGITUDE.value] = tracks.data.apply(
            lambda row: add_distance_to_longitude(long, lat, row[MetaColumn.X_POSITION.value],
                                                  row[MetaColumn.Y_POSITION.value],
                                                  head), axis=1)

    def get_concrete_fatal_corrupts(self, recording_meta: DataRecord, track_meta: DataRecord, tracks: DataRecord,
                                    final_data: DataRecord) -> Dict[FatalCorrupts, List]:

        corrupted_dict: Dict[FatalCorrupts, List] = defaultdict(list)

        if MetaColumn.X_POSITION.value not in tracks.data:
            corrupted_dict[FatalCorrupts.REQUIRED_ROW_MISSING].append(MetaColumn.X_POSITION)
        if MetaColumn.Y_POSITION.value not in tracks.data:
            corrupted_dict[FatalCorrupts.REQUIRED_ROW_MISSING].append(MetaColumn.Y_POSITION)

        return corrupted_dict

    def get_concrete_repairable_corrupts(self, recording_meta: DataRecord, track_meta: DataRecord, tracks: DataRecord,
                                         final_data: DataRecord) -> Dict[ReparableCorrupts, List]:
        corrupted_dict: Dict[ReparableCorrupts, List] = defaultdict(list)

        y_column: pd.DataFrame = tracks.data[MetaColumn.X_POSITION.value]
        x_column: pd.DataFrame = tracks.data[MetaColumn.Y_POSITION.value]

        corrupted_dict[ReparableCorrupts.INVALID_NUMBER].extend(print_non_numeric_rows(x_column))
        corrupted_dict[ReparableCorrupts.INVALID_NUMBER].extend(print_non_numeric_rows(y_column))

        return corrupted_dict

    def concrete_repair(self, recording_meta: DataRecord, track_meta: DataRecord, tracks: DataRecord,
                        final_data: DataRecord) -> bool:
        y_column: pd.DataFrame = tracks.data[MetaColumn.X_POSITION.value]
        x_column: pd.DataFrame = tracks.data[MetaColumn.Y_POSITION.value]

        tracks.data[MetaColumn.X_POSITION.value] = repair_number_column(x_column, DEF_X_LOC)
        tracks.data[MetaColumn.Y_POSITION.value] = repair_number_column(y_column, DEF_Y_LOC)

        return True


class Speed(ColumnHandler):
    """
    this column handler is responsible for the speed
    """

    def get_valid_column(self) -> List[Column]:
        return [Column.SPEED]

    def transfer_column(self, recording_meta: DataRecord, track_meta: DataRecord, tracks: DataRecord,
                        final_data: DataRecord):
        final_data.data[Column.SPEED.value] = numpy.hypot(tracks.data[MetaColumn.X_VELOCITY.value], tracks.data[
            MetaColumn.Y_VELOCITY.value]) * SPEED_MULT

    def get_concrete_fatal_corrupts(self, recording_meta: DataRecord, track_meta: DataRecord, tracks: DataRecord,
                                    final_data: DataRecord) -> Dict[FatalCorrupts, List]:

        corrupted_dict: Dict[FatalCorrupts, List] = defaultdict(list)

        if MetaColumn.X_VELOCITY.value not in tracks.data:
            corrupted_dict[FatalCorrupts.REQUIRED_ROW_MISSING].append(MetaColumn.X_VELOCITY)
        if MetaColumn.Y_VELOCITY.value not in tracks.data:
            corrupted_dict[FatalCorrupts.REQUIRED_ROW_MISSING].append(MetaColumn.Y_VELOCITY)

        return corrupted_dict

    def get_concrete_repairable_corrupts(self, recording_meta: DataRecord, track_meta: DataRecord, tracks: DataRecord,
                                         final_data: DataRecord) -> Dict[ReparableCorrupts, List]:
        corrupted_dict: Dict[ReparableCorrupts, List] = defaultdict(list)

        x_column: pd.DataFrame = tracks.data[MetaColumn.X_VELOCITY.value]
        y_column: pd.DataFrame = tracks.data[MetaColumn.Y_VELOCITY.value]

        corrupted_dict[ReparableCorrupts.INVALID_NUMBER].extend(print_non_numeric_rows(x_column))
        corrupted_dict[ReparableCorrupts.INVALID_NUMBER].extend(print_non_numeric_rows(y_column))

        return corrupted_dict

    def concrete_repair(self, recording_meta: DataRecord, track_meta: DataRecord, tracks: DataRecord,
                        final_data: DataRecord) -> bool:
        y_column: pd.DataFrame = tracks.data[MetaColumn.X_VELOCITY.value]
        x_column: pd.DataFrame = tracks.data[MetaColumn.Y_VELOCITY.value]

        tracks.data[MetaColumn.X_VELOCITY.value] = repair_number_column(x_column, DEF_X_SPEED)
        tracks.data[MetaColumn.Y_VELOCITY.value] = repair_number_column(y_column, DEF_Y_SPEED)

        return True


class Acceleration(ColumnHandler):
    """
    this column handler is responsible for the acceleration
    """

    def get_valid_column(self) -> List[Column]:
        return [Column.ACCELERATION]

    def transfer_column(self, recording_meta: DataRecord, track_meta: DataRecord, tracks: DataRecord,
                        final_data: DataRecord):
        final_data.data[Column.ACCELERATION.value] = numpy.hypot(tracks.data[MetaColumn.X_ACCELERATION.value],
                                                                 tracks.data[MetaColumn.Y_ACCELERATION.value])

    def get_concrete_fatal_corrupts(self, recording_meta: DataRecord, track_meta: DataRecord, tracks: DataRecord,
                                    final_data: DataRecord) -> Dict[FatalCorrupts, List]:

        corrupted_dict: Dict[FatalCorrupts, List] = defaultdict(list)

        if MetaColumn.X_ACCELERATION.value not in tracks.data:
            corrupted_dict[FatalCorrupts.REQUIRED_ROW_MISSING].append(MetaColumn.X_ACCELERATION)
        if MetaColumn.Y_ACCELERATION.value not in tracks.data:
            corrupted_dict[FatalCorrupts.REQUIRED_ROW_MISSING].append(MetaColumn.Y_ACCELERATION)

        return corrupted_dict

    def get_concrete_repairable_corrupts(self, recording_meta: DataRecord, track_meta: DataRecord, tracks: DataRecord,
                                         final_data: DataRecord) -> Dict[ReparableCorrupts, List]:
        corrupted_dict: Dict[ReparableCorrupts, List] = defaultdict(list)

        x_column: pd.DataFrame = tracks.data[MetaColumn.X_ACCELERATION.value]
        y_column: pd.DataFrame = tracks.data[MetaColumn.Y_ACCELERATION.value]

        corrupted_dict[ReparableCorrupts.INVALID_NUMBER].extend(print_non_numeric_rows(x_column))
        corrupted_dict[ReparableCorrupts.INVALID_NUMBER].extend(print_non_numeric_rows(y_column))

        return corrupted_dict

    def concrete_repair(self, recording_meta: DataRecord, track_meta: DataRecord, tracks: DataRecord,
                        final_data: DataRecord) -> bool:
        x_column: pd.DataFrame = tracks.data[MetaColumn.X_ACCELERATION.value]
        y_column: pd.DataFrame = tracks.data[MetaColumn.Y_ACCELERATION.value]

        tracks.data[MetaColumn.X_ACCELERATION.value] = repair_number_column(x_column, DEF_X_ACC)
        tracks.data[MetaColumn.Y_ACCELERATION.value] = repair_number_column(y_column, DEF_Y_ACC)

        return True


class SpeedDirection(ColumnHandler):
    """
    this column handler is responsible for the speed direction
    """

    def get_valid_column(self) -> List[Column]:
        return [Column.SPEED_DIRECTION]

    def transfer_column(self, recording_meta: DataRecord, track_meta: DataRecord, tracks: DataRecord,
                        final_data: DataRecord):

        location_id: Dict[str, float] = LOCATION_IDS[recording_meta.data[MetaColumn.LOCATION_ID.value][0]]
        head: float = location_id[HEAD] + HEAD_OFFSET

        final_data.data[Column.SPEED_DIRECTION.value] = calculate_drection(tracks.data[MetaColumn.X_VELOCITY.value],
                                                                           tracks.data[MetaColumn.Y_VELOCITY.value],
                                                                           head)
        return True

    def get_concrete_fatal_corrupts(self, recording_meta: DataRecord, track_meta: DataRecord, tracks: DataRecord,
                                    final_data: DataRecord) -> Dict[FatalCorrupts, List]:

        corrupted_dict: Dict[FatalCorrupts, List] = defaultdict(list)

        if MetaColumn.X_VELOCITY.value not in tracks.data:
            corrupted_dict[FatalCorrupts.REQUIRED_ROW_MISSING].append(MetaColumn.X_VELOCITY)
        if MetaColumn.Y_VELOCITY.value not in tracks.data:
            corrupted_dict[FatalCorrupts.REQUIRED_ROW_MISSING].append(MetaColumn.Y_VELOCITY)

        return corrupted_dict

    def get_concrete_repairable_corrupts(self, recording_meta: DataRecord, track_meta: DataRecord, tracks: DataRecord,
                                         final_data: DataRecord) -> Dict[ReparableCorrupts, List]:
        corrupted_dict: Dict[ReparableCorrupts, List] = defaultdict(list)

        x_column: pd.DataFrame = tracks.data[MetaColumn.X_VELOCITY.value]
        y_column: pd.DataFrame = tracks.data[MetaColumn.Y_VELOCITY.value]

        corrupted_dict[ReparableCorrupts.INVALID_NUMBER].extend(print_non_numeric_rows(x_column))
        corrupted_dict[ReparableCorrupts.INVALID_NUMBER].extend(print_non_numeric_rows(y_column))

        return corrupted_dict

    def concrete_repair(self, recording_meta: DataRecord, track_meta: DataRecord, tracks: DataRecord,
                        final_data: DataRecord) -> bool:
        y_column: pd.DataFrame = tracks.data[MetaColumn.X_VELOCITY.value]
        x_column: pd.DataFrame = tracks.data[MetaColumn.Y_VELOCITY.value]

        tracks.data[MetaColumn.X_VELOCITY.value] = repair_number_column(x_column, DEF_X_SPEED_DIR)
        tracks.data[MetaColumn.Y_VELOCITY.value] = repair_number_column(y_column, DEF_Y_SPEED_DIR)

        return True


class AccelerationDirection(ColumnHandler):
    """
    this column handler is responsible for the acceleration direction
    """

    def get_valid_column(self) -> List[Column]:
        return [Column.ACCELERATION_DIRECTION]

    def transfer_column(self, recording_meta: DataRecord, track_meta: DataRecord, tracks: DataRecord,
                        final_data: DataRecord):
        location_id: Dict[str, float] = LOCATION_IDS[recording_meta.data[MetaColumn.LOCATION_ID.value][0]]
        head: float = location_id[HEAD] + HEAD_OFFSET

        final_data.data[Column.ACCELERATION_DIRECTION.value] = calculate_drection(
            tracks.data[MetaColumn.X_ACCELERATION.value], tracks.data[MetaColumn.Y_ACCELERATION.value], head)

    def get_concrete_fatal_corrupts(self, recording_meta: DataRecord, track_meta: DataRecord, tracks: DataRecord,
                                    final_data: DataRecord) -> Dict[FatalCorrupts, List]:

        corrupted_dict: Dict[FatalCorrupts, List] = defaultdict(list)

        if MetaColumn.X_ACCELERATION.value not in tracks.data:
            corrupted_dict[FatalCorrupts.REQUIRED_ROW_MISSING].append(MetaColumn.X_ACCELERATION)
        if MetaColumn.Y_ACCELERATION.value not in tracks.data:
            corrupted_dict[FatalCorrupts.REQUIRED_ROW_MISSING].append(MetaColumn.Y_ACCELERATION)

        return corrupted_dict

    def get_concrete_repairable_corrupts(self, recording_meta: DataRecord, track_meta: DataRecord, tracks: DataRecord,
                                         final_data: DataRecord) -> Dict[ReparableCorrupts, List]:
        corrupted_dict: Dict[ReparableCorrupts, List] = defaultdict(list)

        x_column: pd.DataFrame = tracks.data[MetaColumn.X_ACCELERATION.value]
        y_column: pd.DataFrame = tracks.data[MetaColumn.Y_ACCELERATION.value]

        corrupted_dict[ReparableCorrupts.INVALID_NUMBER].extend(print_non_numeric_rows(x_column))
        corrupted_dict[ReparableCorrupts.INVALID_NUMBER].extend(print_non_numeric_rows(y_column))

        return corrupted_dict

    def concrete_repair(self, recording_meta: DataRecord, track_meta: DataRecord, tracks: DataRecord,
                        final_data: DataRecord) -> bool:
        x_column: pd.DataFrame = tracks.data[MetaColumn.X_ACCELERATION.value]
        y_column: pd.DataFrame = tracks.data[MetaColumn.Y_ACCELERATION.value]

        tracks.data[MetaColumn.X_ACCELERATION.value] = repair_number_column(x_column, DEF_X_ACC_DIR)
        tracks.data[MetaColumn.Y_ACCELERATION.value] = repair_number_column(y_column, DEF_Y_ACC_DIR)

        return True


class Road(ColumnHandler):
    """
    this column handler is responsible for the road type
    """

    def get_valid_column(self) -> List[Column]:
        return [Column.ROAD_TYPE]

    def transfer_column(self, recording_meta: DataRecord, track_meta: DataRecord, tracks: DataRecord,
                        final_data: DataRecord):
        final_data.data[Column.ROAD_TYPE.value] = DEF_ROAD_TYPE.value

    def get_concrete_fatal_corrupts(self, recording_meta: DataRecord, track_meta: DataRecord, tracks: DataRecord,
                                    final_data: DataRecord) -> Dict[FatalCorrupts, List]:
        return {}

    def get_concrete_repairable_corrupts(self, recording_meta: DataRecord, track_meta: DataRecord, tracks: DataRecord,
                                         final_data: DataRecord) -> Dict[ReparableCorrupts, List]:
        return {}

    def concrete_repair(self, recording_meta: DataRecord, track_meta: DataRecord, tracks: DataRecord,
                        final_data: DataRecord) -> bool:
        return True


class RoadId(ColumnHandler):
    """
    this column handler is responsible for the osm road id
    """

    def get_valid_column(self) -> List[Column]:
        return []

    def transfer_column(self, recording_meta: DataRecord, track_meta: DataRecord, tracks: DataRecord,
                        final_data: DataRecord):
        final_data.data[Column.OSM_ROAD_ID.value] = DEF_ROAD_ID

    def get_concrete_fatal_corrupts(self, recording_meta: DataRecord, track_meta: DataRecord, tracks: DataRecord,
                                    final_data: DataRecord) -> Dict[FatalCorrupts, List]:
        return {}

    def get_concrete_repairable_corrupts(self, recording_meta: DataRecord, track_meta: DataRecord, tracks: DataRecord,
                                         final_data: DataRecord) -> Dict[ReparableCorrupts, List]:
        return {}

    def concrete_repair(self, recording_meta: DataRecord, track_meta: DataRecord, tracks: DataRecord,
                        final_data: DataRecord) -> bool:
        return True


class OneWay(ColumnHandler):
    """
    this column handler is responsible for the one way street column
    """

    def get_valid_column(self) -> List[Column]:
        return [Column.ONE_WAY_STREET.value]

    def transfer_column(self, recording_meta: DataRecord, track_meta: DataRecord, tracks: DataRecord,
                        final_data: DataRecord):
        final_data.data[Column.ONE_WAY_STREET.value] = True

    def get_concrete_fatal_corrupts(self, recording_meta: DataRecord, track_meta: DataRecord, tracks: DataRecord,
                                    final_data: DataRecord) -> Dict[FatalCorrupts, List]:
        return {}

    def get_concrete_repairable_corrupts(self, recording_meta: DataRecord, track_meta: DataRecord, tracks: DataRecord,
                                         final_data: DataRecord) -> Dict[ReparableCorrupts, List]:
        return {}

    def concrete_repair(self, recording_meta: DataRecord, track_meta: DataRecord, tracks: DataRecord,
                        final_data: DataRecord) -> bool:
        return True


class Filtered(ColumnHandler):
    """
    this column handler is responsible for the filtered column
    """

    def get_valid_column(self) -> List[Column]:
        return [Column.FILTERED.value]

    def transfer_column(self, recording_meta: pd.DataFrame, track_meta: pd.DataFrame, tracks: pd.DataFrame,
                        final_data: pd.DataFrame):
        final_data.data[Column.FILTERED.value] = False

    def get_concrete_fatal_corrupts(self, recording_meta: DataRecord, track_meta: DataRecord, tracks: DataRecord,
                                    final_data: DataRecord) -> Dict[FatalCorrupts, List]:
        return {}

    def get_concrete_repairable_corrupts(self, recording_meta: DataRecord, track_meta: DataRecord, tracks: DataRecord,
                                         final_data: DataRecord) -> Dict[ReparableCorrupts, List]:
        return {}

    def concrete_repair(self, recording_meta: DataRecord, track_meta: DataRecord, tracks: DataRecord,
                        final_data: DataRecord) -> bool:
        return True


def format_date(date_str):
    """
    converts the data into the right format
    :param date_str:    the date
    :return:            the formatted date
    """
    # remove all dots in the data
    date_str = date_str.replace(".", "")

    formatted_date = ["20", "04", "2020"]

    if len(date_str) >= 4:
        formatted_date[2] = date_str[-4:]

    if len(date_str) >= 5:
        formatted_date[1] = date_str[-5:-4]

        if not len(date_str) >= 6:
            formatted_date[1] = "0" + formatted_date[1]
            return formatted_date

    if len(date_str) >= 6:
        formatted_date[1] = date_str[-6:-4]

    if len(date_str) >= 7:
        formatted_date[0] = date_str[-7:-6]

    if len(date_str) >= 8:
        formatted_date[0] = date_str[-8:-6]

    return formatted_date
