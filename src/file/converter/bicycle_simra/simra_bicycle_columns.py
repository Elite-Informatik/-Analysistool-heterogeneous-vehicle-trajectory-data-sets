from enum import Enum


class SimraColumn(Enum):
    """
    Holds all the columns present in the simra data format.
    """
    LATITUDE = "lat"
    LONGITUDE = "lon"
    X = "X"  #
    Y = "Y"  # accelerometer readings
    Z = "Z"  #
    TIME_STAMP = "timeStamp" # timestamp (number of milliseconds from epoch)
    ACC = "acc"     # the radius of 68% confidence, meaning that there is a 68% chance that the true location is within
                    # that radius of the measured point (lat, lon) in meters
    A = "a"  #
    B = "b"  # gyroscope readings
    C = "c"  #
