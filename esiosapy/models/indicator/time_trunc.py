from enum import Enum


class TimeTrunc(Enum):
    FIVE_MINUTES = "five_minutes"
    TEN_MINUTES = "ten_minutes"
    FIFTHEEN_MINUTES = "fiftheen_minutes"
    HOUR = "hour"
    DAY = "day"
    MONTH = "month"
    YEAR = "year"
