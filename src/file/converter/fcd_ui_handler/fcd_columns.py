from enum import Enum


class FcdColumn(Enum):
    """
    holds all relevant columns of the fcd dataformat
    """

    TRIP = "trip"
    SEG_TYPE = "seg_type"
    DATE_TIME = "fcd_time"
    AZIMUTH = "fcd_azimuth"
    SPEED = "fcd_speed"
    POINT = "fcd_point"
    ROAD_ID = "road_osm_id"
    MAX_SPEED = "road_max_speed"
    ROAD_TYPE = "road_type"
    ROAD_OSM_TYPE = "road_osm_id"
    ONE_WAY_STREET = "road_oneway"
