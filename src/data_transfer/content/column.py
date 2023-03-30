from enum import Enum
from typing import List
from typing import Optional

data_types = {
    'id': 'INT PRIMARY KEY',
    'trajectory_id': 'INT NOT NULL',
    'date': 'DATE NOT NULL',
    'time': 'DATE_TIME NOT NULL',
    'latitude': 'FLOAT',
    'longitude': 'FLOAT',
    'speed': 'FLOAT',
    'speed_limit': 'FLOAT',
    'acceleration': 'FLOAT',
    'speed_direction': 'FLOAT',
    'acceleration_direction': 'FLOAT',
    'road_type': 'VARCHAR(50)',
    'osm_road_id': 'INT',
    'one_way_street': 'BIT',
    "original_order": "INT"
}

class Column(Enum):
    """
    holds all columns in our unified data format
    """

    ID = 'id'
    TRAJECTORY_ID = 'trajectory_id'
    DATE = 'date'
    TIME = 'time'
    LATITUDE = 'latitude'
    LONGITUDE = 'longitude'
    SPEED = 'speed'
    SPEED_LIMIT = 'speed_limit'
    ACCELERATION = 'acceleration'
    SPEED_DIRECTION = 'speed_direction'
    ACCELERATION_DIRECTION = 'acceleration_direction'
    ROAD_TYPE = 'road_type'
    OSM_ROAD_ID = 'osm_road_id'
    ONE_WAY_STREET = 'one_way_street'
    VEHICLE_TYPE = 'vehicle_type'
    FILTERED = 'filtered'
    ORDER = 'original_order'

    @classmethod
    def list(cls) -> List['Column']:
        """
        returns all items of this enum as list
        """
        return [col for col in Column]

    @classmethod
    def val_list(cls) -> List[str]:
        """
        returns the values of all items of this enum as list
        """
        return [col.value for col in Column]

    @staticmethod
    def get_interval_columns() -> List['Column']:
        """
        gets all items that can be measured in form of an inverval
        """
        return [Column.DATE, Column.TIME, Column.LATITUDE, Column.LONGITUDE,
                Column.SPEED, Column.SPEED_LIMIT, Column.ACCELERATION, Column.SPEED_DIRECTION,
                Column.ACCELERATION_DIRECTION]

    @staticmethod
    def get_discrete_columns() -> List['Column']:
        """
        gets all items that have discrete values
        """
        return [Column.TRAJECTORY_ID, Column.SPEED_LIMIT, Column.ROAD_TYPE, Column.OSM_ROAD_ID,
                Column.ONE_WAY_STREET]

    @staticmethod
    def get_time_interval_columns():
        """
        gets all columns of the type time
        """
        return [Column.TIME]

    @staticmethod
    def get_number_interval_columns():
        """
        gets all columns of the type number
        """
        return [Column.LATITUDE, Column.LONGITUDE, Column.SPEED, Column.SPEED_LIMIT,
                Column.ACCELERATION, Column.SPEED_DIRECTION, Column.ACCELERATION_DIRECTION]

    @staticmethod
    def get_date_interval_columns():
        """
        gets all items of the type date
        """
        return [Column.DATE]

    @classmethod
    def get_column_from_str(cls, column_str: str) -> Optional['Column']:
        """
        gets the item with the given value
        :param column_str: the string value
        :return            the item with the given string value
        """
        if column_str not in Column.val_list():
            return None
        return [col for col in Column if col.value == column_str][0]

    def __str__(self):
        value = f'{self._value_}'
        return value.replace("_", " ")

    def __repr__(self):
        return self.__str__()


# map that maps all interval filterable columns to the valid value ranges
COLUM_TO_VALUE_RANGE = {
    Column.DATE: (None, None),
    Column.TIME: (None, None),
    Column.SPEED: (None, None),
    Column.SPEED_LIMIT: (None, None),
    Column.SPEED_DIRECTION: (0, 360),
    Column.ID: (None, None),
    Column.TRAJECTORY_ID: (None, None),
    Column.LATITUDE: (-90, 90),
    Column.LONGITUDE: (-180, 180),
    Column.ACCELERATION: (None, None),
    Column.ACCELERATION_DIRECTION: (None, None),
}

