import math
import random
import time
from random import randint
from random import uniform
from uuid import UUID
from uuid import uuid4

import pandas as pd
from pandas import DataFrame

from src.data_transfer.content.column import Column
from src.file.file_facade_manager import DataRecord
from src.file.file_facade_manager import FileFacadeManager


class DataGenerator:
    CURRENT_ID = uuid4()
    TRAJECTORY_ID = uuid4()
    TIME = time.mktime(time.strptime("01:00:00", "%H:%M:%S"))
    LONG = round(uniform(-1, 1), 6)
    LAT = round(uniform(-1, 1), 6)
    SPEED = round(uniform(0, 0.1), 6)
    SPEED_DIR = round(uniform(0, 360), 6)
    ACCELERATION = round(uniform(0, 0.01), 6)
    ACCELERATION_DIR = round(uniform(0, 360), 6)

    def __init__(self):
        self._time_difference = 0

    def generate_data_point(self) -> DataFrame:
        id = self.make_id()
        data = {
            Column.ID.value: id,
            Column.TRAJECTORY_ID.value: self.make_trajectory_id(),
            Column.DATE.value: "01.01.2023",
            Column.TIME.value: self.make_time(),
            Column.LATITUDE.value: self.make_latitude(),
            Column.LONGITUDE.value: self.make_longitude(),
            Column.SPEED.value: self.make_speed(),
            Column.SPEED_LIMIT.value: self.make_limit(),
            Column.ACCELERATION.value: self.make_acceleration(),
            Column.SPEED_DIRECTION.value: self.make_speed_dir(),
            Column.ACCELERATION_DIRECTION.value: self.make_acceleration_direction(),
            Column.ROAD_TYPE.value: self.make_road_type(),
            Column.ONE_WAY_STREET.value: False,
            Column.OSM_ROAD_ID.value: None,
            Column.VEHICLE_TYPE.value: "Autooo",
            Column.FILTERED.value: False
        }
        d = pd.DataFrame(data, index=[id])
        return d

    def generate_test_data(self, lines: int = 1) -> DataFrame:
        d = self.generate_data_point()
        for i in range(lines - 1):
            d = pd.concat([d, self.generate_data_point()], ignore_index=True)
        return d

    def make_id(self) -> UUID:
        return uuid4()

    def make_trajectory_id(self) -> UUID:
        if randint(0, 50) == 50:
            self.TRAJECTORY_ID = uuid4()
            self.LONG = round(uniform(-1, 1), 6)
            self.LAT = round(uniform(-1, 1), 6)
            self.SPEED = round(uniform(0, 0.1), 6)
            self.SPEED_DIR = round(uniform(0, 0.01), 6)
        return self.TRAJECTORY_ID

    def make_time(self) -> int:
        self._time_difference = randint(0, 50)
        self.TIME += self._time_difference
        return time.strftime("%H:%M:%S", time.gmtime(self.TIME))

    def make_latitude(self):
        self.LAT += math.cos(self.SPEED_DIR) * (self._time_difference / 3600 * self.SPEED)
        if self.LAT > 180:
            self.LAT -= 360
        elif self.LAT < -180:
            self.LAT += 360
        return self.LAT

    def make_longitude(self):
        self.LONG += math.sin(self.SPEED_DIR) * (self._time_difference / 3600 * self.SPEED)
        if self.LONG > 90:
            self.LONG -= 180
        elif self.LONG < -90:
            self.LONG += 180
        return self.LONG

    def make_speed(self):
        return self.SPEED

    def make_speed_dir(self):
        return self.SPEED_DIR

    def make_limit(self):
        return random.choice([30, 50, 70, 80, 90, 120, 130, 20000])

    def make_acceleration(self):
        return self.ACCELERATION

    def make_acceleration_direction(self):
        return self.ACCELERATION_DIR

    def make_road_type(self):
        return None


if __name__ == "__main__":
    generator = DataGenerator()
    file_facade = FileFacadeManager()
    file_facade.export_data_file(
        path="/Users/julianheines/PycharmProjects/Analysistool-heterogeneous-vehicle-trajectory-data-sets/test/file",
        data=DataRecord("intern_data_performance_test", None, generator.generate_test_data(10000)),
        file_format="csv")
