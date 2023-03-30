import random
from typing import List
from uuid import UUID
from uuid import uuid4

import pandas as pd

from src.controller.output_handling.event import DatasetDeleted
from src.controller.output_handling.event import PolygonAdded
from src.controller.output_handling.event import PolygonDeleted
from src.data_transfer.record import DataPointRecord
from src.data_transfer.record import DataRecord
from src.data_transfer.record import DatasetRecord
from src.data_transfer.record import PageRecord
from src.data_transfer.record import PolygonRecord
from src.data_transfer.record import PositionRecord
from src.data_transfer.record import SegmentRecord
from src.data_transfer.record import SelectionRecord
from src.data_transfer.record import SettingRecord
from src.data_transfer.record import SettingsRecord
from src.data_transfer.record import TrajectoryRecord
from src.data_transfer.selection import BoolDiscreteOption
from src.view.event_handler import EventHandler

"""from src.controller.event import PolygonDeleted, PolygonAdded, DatasetDeleted
from src.data_transfer import PolygonRecord, DataRecord
from src.view.event_handler import EventHandler
from src.data_transfer import PositionRecord
from src.data_transfer import DatasetRecord
from src.data_transfer import TrajectoryRecord, DataPointRecord"""


def create_random_poly():
    return [(random.randint(-80, 80), random.randint(-80, 80)) for i in range(random.randint(3, 7))]


def create_random_position_record():
    return PositionRecord(_latitude=random.uniform(51, 53), _longitude=random.uniform(13, 15))


def create_random_datapoint_record():
    rand = random.randint(0, 1)
    if rand == 0:
        filtered = False
    if rand == 1:
        filtered = True
    return DataPointRecord(_uuid=uuid4(), _position=create_random_position_record(),
                           _visualisation=random.randint(0, 2000),
                           _filtered=filtered)


def create_random_trajectory_record():
    datapoints = [create_random_datapoint_record() for _ in range(random.randint(100, 100))]
    return TrajectoryRecord(_id=uuid4(), _datapoints=tuple(datapoints))


class ControllerStump:

    def __init__(self, event_handler: EventHandler):
        self._event_handler = event_handler

    def delete_polygon(self, uuid: UUID):
        self._event_handler.notify_event(PolygonDeleted(uuid))
        DataRequestStump.added_polygon_via_map = False
        self._event_handler.notify_event(PolygonAdded(uuid))

    def add_polygon(self, position_list: List, name: str):
        DataRequestStump.name = name
        DataRequestStump.polygon = position_list
        DataRequestStump.added_polygon_via_map = True
        self._event_handler.notify_event(PolygonAdded(uuid4()))

    def delete_dataset(self, uuid: UUID):
        self._event_handler.notify_event(DatasetDeleted(_id=uuid))

    def close_application(self):
        print("close_application")


class DataRequestStump:
    added_polygon_via_map = False
    polygon = []
    name = ""

    def __init__(self):
        self._id_datasets1 = uuid4()
        self._id_datasets2 = uuid4()
        self._id_datasets3 = uuid4()

        self._datasets = {
            self._id_datasets1: DatasetRecord(_name="datensatz1", _size=1000),
            self._id_datasets2: DatasetRecord(_name="datensatz2", _size=2000),
            self._id_datasets3: DatasetRecord(_name="datensatz3", _size=3000)
        }

    def get_polygon(self, id):
        if self.added_polygon_via_map:
            corners = []
            for position in DataRequestStump.polygon:
                corners.append(PositionRecord(position[0], position[1]))
            polygon = PolygonRecord(_corners=corners, _name=DataRequestStump.name)
            return polygon
        else:
            position_list = create_random_poly()
            corners = []
            for position in position_list:
                corners.append(PositionRecord(position[0], position[1]))
            return PolygonRecord(_corners=tuple(corners), _name="polygon")

    def get_dataset_meta(self, id):
        return self._datasets[id]

    def get_dataset_ids(self):
        return self._datasets.keys()

    def get_settings(self):
        selection = SelectionRecord(selected=[True], option=BoolDiscreteOption())
        setting = SettingRecord(_context=",", _selection=selection, _identifier="show_line_segments")
        segments = SegmentRecord(_settings=[setting], _identifier="", _name="")
        page_record = PageRecord(_segments=[segments], _identifier="", _name="")
        return SettingsRecord(_pages=[page_record])

    def get_shown_trajectories(self) -> List[TrajectoryRecord]:
        return [create_random_trajectory_record() for _ in range(random.randint(10, 10))]

    def get_root_trajectory_filter(self):
        return uuid4()

    def get_root_datapoint_filter(self):
        return uuid4()

    def get_trajectory_data(self, trajectory_id: UUID) -> DataRecord:
        data_frame = pd.DataFrame(columns=["A", "B", "C"], data=[[10, 100, 1000], [20, 4235, 333], [3235555, 10, -9]])
        return DataRecord(_name="trajectroy data", _column_names=tuple(data_frame.columns.to_list()), _data=data_frame)

    def get_datapoint_data(self, datapoint_id: UUID) -> DataRecord:
        data_frame = pd.DataFrame(columns=["A", "B", "C"], data=[[10, 30, -1000]])
        return DataRecord(_name="trajectory data", _column_names=tuple(data_frame.columns.tolist()), _data=data_frame)
