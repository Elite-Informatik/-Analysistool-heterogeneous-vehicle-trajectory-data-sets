from dataclasses import dataclass
from typing import List
from typing import Tuple

from src.data_transfer.record.position_record import PositionRecord


@dataclass(frozen=True)
class PolygonRecord:
    """
    record holding all information about a polygon
    """

    _corners: Tuple[PositionRecord, ...]
    _name: str

    @property
    def corners(self) -> Tuple[PositionRecord, ...]:
        """
        the list of corners
        """
        return self._corners

    @property
    def name(self) -> str:
        """
        the name
        """
        return self._name

    def get_positions_as_list(self) -> List[Tuple[float, float]]:
        """
        all coordinates of the corners
        """
        return [(position.latitude, position.longitude) for position in self.corners]

    def __repr__(self):
        return self._name
