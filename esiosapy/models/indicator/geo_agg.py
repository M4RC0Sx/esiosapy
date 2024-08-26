from enum import Enum


class GeoAgg(Enum):
    """
    Enum representing the types of geographical aggregation methods.

    This enum defines the methods that can be used to aggregate geographical data,
    such as summing values or calculating their average.

    :cvar SUM: Represents the aggregation method that sums up the values.
    :vartype SUM: str
    :cvar AVERAGE: Represents the aggregation method that calculates
                   the average of the values.
    :vartype AVERAGE: str
    """

    SUM = "sum"
    """Represents the aggregation method that sums up the values."""

    AVERAGE = "average"
    """Represents the aggregation method that calculates the average of the values."""
