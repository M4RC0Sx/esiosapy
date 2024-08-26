from enum import Enum


class TimeAgg(Enum):
    """
    Enum representing the types of temporal aggregation methods.

    This enum defines the methods that can be used to aggregate data over time,
    such as summing values or calculating their average.

    :cvar SUM: Represents the aggregation method that sums up the values over time.
    :vartype SUM: str
    :cvar AVERAGE: Represents the aggregation method that calculates
                   the average of the values over time.
    :vartype AVERAGE: str
    """

    SUM = "sum"
    """Represents the aggregation method that sums up the values."""

    AVERAGE = "average"
    """Represents the aggregation method that calculates the avg of the values."""
