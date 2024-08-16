import os
from datetime import datetime, date
from pathlib import Path
from typing import List, Dict, Any, Union

from pydantic import BaseModel

from esiosapy.models.archive.archive_download import ArchiveDownload
from esiosapy.models.archive.taxonomy_term import TaxonomyTerm
from esiosapy.models.archive.vocabulary import Vocabulary

from esiosapy.utils.request_helper import RequestHelper
from esiosapy.utils.zip_utils import recursive_unzip


class Archive(BaseModel):
    id: int
    name: str
    horizon: str
    archive_type: str
    download: ArchiveDownload
    _date: datetime
    date_times: List[date] = []
    publication_date: List[date] = []
    taxonomy_terms: List[TaxonomyTerm] = []
    vocabularies: List[Vocabulary] = []
    raw: Dict[str, Any]

    _request_helper: RequestHelper

    def __init__(self, **data: Any):
        super().__init__(**data)
        self._request_helper = data["_request_helper"]

    def download_file(
        self,
        path: Union[str, Path] = Path.cwd(),
        unzip: bool = True,
        remove_zip: bool = True,
    ) -> None:
        response = self._request_helper.get_request(self.download.url)

        zip_path = Path(os.path.join(path, f"{self.name}.zip"))

        with open(zip_path, "wb") as f:
            f.write(response.content)

        if unzip:
            recursive_unzip(zip_path, zip_path.stem, remove=remove_zip)
