from dataclasses import dataclass
from typing import List
from typing import Tuple
from uuid import UUID

from src.data_transfer.record import DataPointRecord


@dataclass(frozen=True)
class TrajectoryRecord:
    """
    record that holds all information of a trajectory
    """

    _datapoints: Tuple[DataPointRecord, ...]
    _id: UUID

    @property
    def datapoints(self):
        """
        the contained datapoints
        """
        return self._datapoints

    @property
    def id(self):
        """
        the trajectory id
        """
        return self._id

    def get_positions_as_list(self) -> List:
        """
        gets the positions of the contained datapoints as list
        """
        return [datapoint.get_position_as_tuple() for datapoint in self._datapoints]

    def get_latitudes(self) -> List[float]:
        return [datapoint.position.latitude for datapoint in self._datapoints]

    def get_longitudes(self) -> List[float]:
        return [datapoint.position.longitude for datapoint in self._datapoints]
