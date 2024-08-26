from enum import Enum


class TimeTrunc(Enum):
    """
    Enum representing the types of temporal truncation levels.

    This enum defines various levels of time intervals that can be used to truncate or
    categorize data, ranging from five minutes to a full year.

    :cvar FIVE_MINUTES: Represents the five-minute level of temporal truncation.
    :vartype FIVE_MINUTES: str
    :cvar TEN_MINUTES: Represents the ten-minute level of temporal truncation.
    :vartype TEN_MINUTES: str
    :cvar FIFTHEEN_MINUTES: Represents the fifteen-minute level of temporal truncation.
    :vartype FIFTHEEN_MINUTES: str
    :cvar HOUR: Represents the hourly level of temporal truncation.
    :vartype HOUR: str
    :cvar DAY: Represents the daily level of temporal truncation.
    :vartype DAY: str
    :cvar MONTH: Represents the monthly level of temporal truncation.
    :vartype MONTH: str
    :cvar YEAR: Represents the yearly level of temporal truncation.
    :vartype YEAR: str
    """

    FIVE_MINUTES = "five_minutes"
    """Represents the five-minute level of temporal truncation."""

    TEN_MINUTES = "ten_minutes"
    """Represents the ten-minute level of temporal truncation."""

    FIFTHEEN_MINUTES = "fiftheen_minutes"
    """Represents the fifteen-minute level of temporal truncation."""

    HOUR = "hour"
    """Represents the hourly level of temporal truncation."""

    DAY = "day"
    """Represents the daily level of temporal truncation."""

    MONTH = "month"
    """Represents the monthly level of temporal truncation."""

    YEAR = "year"
    """Represents the yearly level of temporal truncation."""
