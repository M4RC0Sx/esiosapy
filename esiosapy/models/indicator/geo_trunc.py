from enum import Enum


class GeoTrunc(Enum):
    """
    Enum representing the types of geographical truncation levels.

    This enum defines various levels of geographical regions that can be used to
    truncate or categorize data, ranging from broad areas like countries to more
    specific regions like towns or drainage basins.

    :cvar COUNTRY: Represents the country level of geographical truncation.
    :vartype COUNTRY: str
    :cvar ELECTRIC_SYSTEM: Represents the electric system level
                           of geographical truncation.
    :vartype ELECTRIC_SYSTEM: str
    :cvar AUTONOMOUS_COMMUNITY: Represents the autonomous community
                                level of geographical truncation.
    :vartype AUTONOMOUS_COMMUNITY: str
    :cvar PROVINCE: Represents the province level of geographical truncation.
    :vartype PROVINCE: str
    :cvar ELECTRIC_SUBSYSTEM: Represents the electric subsystem level
                              of geographical truncation.
    :vartype ELECTRIC_SUBSYSTEM: str
    :cvar TOWN: Represents the town level of geographical truncation.
    :vartype TOWN: str
    :cvar DRAINAGE_BASIN: Represents the drainage basin level
                          of geographical truncation.
    :vartype DRAINAGE_BASIN: str
    """

    COUNTRY = "country"
    """Represents the country level of geographical truncation."""

    ELECTRIC_SYSTEM = "electric_system"
    """Represents the electric system level of geographical truncation."""

    AUTONOMOUS_COMMUNITY = "autonomous_community"
    """Represents the autonomous community level of geographical truncation."""

    PROVINCE = "province"
    """Represents the province level of geographical truncation."""

    ELECTRIC_SUBSYSTEM = "electric_subsystem"
    """Represents the electric subsystem level of geographical truncation."""

    TOWN = "town"
    """Represents the town level of geographical truncation."""

    DRAINAGE_BASIN = "drainage_basin"
    """Represents the drainage basin level of geographical truncation."""
