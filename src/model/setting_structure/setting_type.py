from enum import Enum


class Color(Enum):
    """
    An enumeration of different color modes that can be used in a visualization.

    This enumeration is used to represent the different color modes that can be used when creating a visualization. The
    possible values are "Random", "Parameter", and "Uni". These values are used to specify how the colors in the
    visualization should be determined.
    """
    RANDOM = "Random color"
    UNI = "Uni-color"
    PARAMETER = "Parameter"

    def __repr__(self):
        return self.value
