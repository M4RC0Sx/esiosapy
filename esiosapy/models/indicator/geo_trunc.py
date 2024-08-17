from enum import Enum


class GeoTrunc(Enum):
    COUNTRY = "country"
    ELECTRIC_SYSTEM = "electric_system"
    AUTONOMOUS_COMMUNITY = "autonomous_community"
    PROVINCE = "province"
    ELECTRIC_SUBSYSTEM = "electric_subsystem"
    TOWN = "town"
    DRAINAGE_BASIN = "drainage_basin"
