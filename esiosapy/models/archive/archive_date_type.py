from enum import Enum


class ArchiveDateType(Enum):
    """
    Enum representing the types of dates associated with an archive.

    This enum defines two types of dates that can be used to categorize or filter
    archives: the date the data was recorded and the date the data was published.

    :cvar DATA: Represents the date when the data was recorded or collected.
    :vartype DATA: str
    :cvar PUBLICATION: Represents the date when the data was published.
    :vartype PUBLICATION: str
    """

    DATA = "datos"
    """Represents the date when the data applies."""

    PUBLICATION = "publicacion"
    """Represents the date when the data was published."""
