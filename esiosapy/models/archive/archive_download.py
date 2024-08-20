from dataclasses import dataclass


@dataclass
class ArchiveDownload:
    """
    Represents the download information for an archive.

    This dataclass contains information about the downloadable content associated
    with an archive, including
    the name of the file and the URL where it can be accessed.
    """

    name: str
    """The name of the file to be downloaded.

    :type: str
    """

    url: str
    """The URL where the file can be downloaded.

    :type: str
    """
