import os
from datetime import date, datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel

from esiosapy.models.archive.archive_download import ArchiveDownload
from esiosapy.models.archive.taxonomy_term import TaxonomyTerm
from esiosapy.models.archive.vocabulary import Vocabulary
from esiosapy.utils.request_helper import RequestHelper
from esiosapy.utils.zip_utils import recursive_unzip


class Archive(BaseModel):
    """
    Represents an archive with metadata and methods to download associated files.

    This class models an archive object with various attributes such as its ID, name,
    type, and associated download information. It also provides a method to download
    the archive file, with options to unzip the file and remove the original zip file.
    """

    id: int
    """The unique identifier for the archive.

    :type: int
    """

    name: str
    """The name of the archive.

    :type: str
    """

    horizon: str
    """The horizon associated with the archive.

    :type: str
    """

    archive_type: str
    """The type/category of the archive.

    :type: str
    """

    download: ArchiveDownload
    """The download information associated with the archive.

    :type: ArchiveDownload
    """

    _date: datetime
    """The date associated with the archive.

    :type: datetime
    """

    date_times: List[date] = []
    """A list of dates associated with the archive.

    :type: List[date]
    """

    publication_date: List[date] = []
    """A list of publication dates for the archive.

    :type: List[date]
    """

    taxonomy_terms: List[TaxonomyTerm] = []
    """A list of taxonomy terms associated with the archive.

    :type: List[TaxonomyTerm]
    """

    vocabularies: List[Vocabulary] = []
    """A list of vocabularies associated with the archive.

    :type: List[Vocabulary]
    """

    raw: Dict[str, Any]
    """The raw data from which the archive object was created.

    :type: Dict[str, Any]
    """

    _request_helper: RequestHelper
    """An instance of RequestHelper used to make API requests.

    :type: RequestHelper
    """

    def __init__(self, **data: Any):
        """
        Initializes the Archive object with the provided data.

        :param data: The data used to initialize the Archive object. This includes
                     all the attributes as well as a RequestHelper instance
                     for making API requests.
        :type data: Any
        """
        super().__init__(**data)
        self._request_helper = data["_request_helper"]

    def download_file(
        self,
        path: Optional[Union[str, Path]] = None,
        unzip: bool = True,
        remove_zip: bool = True,
    ) -> None:
        """
        Downloads the archive file and optionally unzips it.

        This method downloads the file associated with the archive to the specified
        path. The file can be automatically unzipped and the original zip file can
        be removed based on the provided options.

        :param path: The directory where the file should be downloaded. If not provided,
                     the current working directory is used.
        :type path: Optional[Union[str, Path]], optional
        :param unzip: Whether to unzip the downloaded file, defaults to True.
        :type unzip: bool, optional
        :param remove_zip: Whether to remove the original zip file after unzipping,
                           defaults to True.
        :type remove_zip: bool, optional
        :return: None
        """
        if path is None:
            path = Path.cwd()

        response = self._request_helper.get_request(self.download.url)

        zip_path = Path(os.path.join(path, f"{self.name}.zip"))

        with open(zip_path, "wb") as f:
            f.write(response.content)

        if unzip:
            recursive_unzip(zip_path, zip_path.stem, remove=remove_zip)
