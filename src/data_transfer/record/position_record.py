from dataclasses import dataclass

from typing import List


@dataclass(frozen=True)
class PositionRecord:
    """
    record containing a position
    """

    _latitude: float
    _longitude: float

    @property
    def latitude(self):
        """
        the latitude
        """
        return self._latitude

    @property
    def longitude(self):
        """
        the longitude
        """
        return self._longitude

    def to_tuple(self) -> List[float]:
        """
        the position as tuple (latitude, longitude)
        """
        return [self.latitude, self.longitude]

    def __str__(self):
        # Needed in : _create_polygon_filter_strs of filter_visitor class, very practical
        return str(self._latitude) + " " + str(self._longitude)
