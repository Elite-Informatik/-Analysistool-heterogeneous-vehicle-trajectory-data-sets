from dataclasses import dataclass
from typing import List
from uuid import UUID

from src.data_transfer.record.position_record import PositionRecord


@dataclass(frozen=True)
class DataPointRecord:
    """
    record that holds all information of a datapoint
    """
    _uuid: UUID
    _position: PositionRecord
    _visualisation: int
    _filtered: bool

    @property
    def position(self):
        """
        the coordinates of this datapoint
        """
        return self._position

    @property
    def id(self):
        """
        the id of the datapoint
        """
        return self._uuid

    @property
    def visualisation(self):
        """
        how the datapoint should be visualised
        """
        return self._visualisation

    @property
    def filtered(self):
        """
        whether the datapoint was filtered out
        """
        return self._filtered

    def get_position_as_tuple(self) -> List:
        """
        gets the coordinates as tuple [x, y]
        """
        return self._position.to_tuple()
