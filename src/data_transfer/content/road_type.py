from enum import Enum


class RoadType(Enum):
    """
    holds all available road types
    """

    LIVING_STREET = "Living street"
    MOTORWAY = "Motorway"
    MOTORWAY_LINK = "Motorway link"
    SECONDARY = "Secondary"
    SECONDARY_LINK = "Secondary link"
    TRUNK = "Trunk"
    TRUNK_LINK = "Trunk link"
    RESIDENTIAL = "Residential"
    SERVICE = "Service"
    PRIMARY = "Primary"
    PRIMARY_LINK = "Primary link"
    TERTIARY = "Tertiary"
    TERTIARY_LINK = "Tertiary"
    UNCLASSIFIED = "Unclassified"

    def __str__(self):
        return self._value_

    def __repr__(self):
        return self.__str__()


class VehicleType(Enum):
    """
    holds all available vehicle types
    """

    CAR = "Car"
    TRUCK = "Truck"
    BICYCLE = "Bicycle"
    MOTORCYCLE = "Motorcycle"
    BUS = "Bus"
    UNKNOWN = "Unknown"
