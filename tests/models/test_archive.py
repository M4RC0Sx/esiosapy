from __future__ import annotations

from datetime import date
from datetime import datetime
from typing import TYPE_CHECKING
from typing import Any

import pytest

from esiosapy.models.archive.archive import Archive
from esiosapy.models.archive.archive_date_type import ArchiveDateType
from esiosapy.models.archive.archive_download import ArchiveDownload
from esiosapy.models.archive.taxonomy_term import TaxonomyTerm
from esiosapy.models.archive.vocabulary import Vocabulary


if TYPE_CHECKING:
    from pytest_mock import MockerFixture


class TestArchiveDownload:
    def test_initialization(self) -> None:
        download = ArchiveDownload(name="test.zip", url="https://example.com/test.zip")
        assert download.name == "test.zip"
        assert download.url == "https://example.com/test.zip"


class TestTaxonomyTerm:
    def test_initialization(self) -> None:
        term = TaxonomyTerm(id_taxonomy_term=1, name="energy", vocabulary_id=1)
        assert term.id_taxonomy_term == 1
        assert term.name == "energy"
        assert term.vocabulary_id == 1


class TestVocabulary:
    def test_initialization(self) -> None:
        vocab = Vocabulary(id_vocabulary=1, name="power")
        assert vocab.id_vocabulary == 1
        assert vocab.name == "power"


class TestArchiveDateTypeValues:
    def test_values(self) -> None:
        assert ArchiveDateType.DATA.value == "datos"
        assert ArchiveDateType.PUBLICATION.value == "publicacion"


class TestArchive:
    @pytest.fixture
    def mock_request_helper(self, mocker: MockerFixture) -> object:
        return mocker.MagicMock()

    @pytest.fixture
    def archive_data(self, mock_request_helper: object) -> dict[str, Any]:
        return {
            "id": 1,
            "name": "Test Archive",
            "horizon": "daily",
            "archive_type": "data",
            "download": {
                "name": "test_archive.zip",
                "url": "https://example.com/archive.zip",
            },
            "date": datetime(2024, 1, 15, 10, 0, 0),
            "date_times": [date(2024, 1, 15)],
            "publication_date": [date(2024, 1, 14)],
            "taxonomy_terms": [
                {"id_taxonomy_term": 1, "name": "energy", "vocabulary_id": 1}
            ],
            "vocabularies": [{"id_vocabulary": 1, "name": "power"}],
            "raw": {"key": "value"},
            "_request_helper": mock_request_helper,
        }

    def test_initialization(self, archive_data: dict[str, Any]) -> None:
        archive = Archive(**archive_data)
        assert archive.id == 1
        assert archive.name == "Test Archive"
        assert archive.horizon == "daily"
        assert archive.archive_type == "data"

    def test_download_attribute(self, archive_data: dict[str, Any]) -> None:
        archive = Archive(**archive_data)
        assert isinstance(archive.download, ArchiveDownload)
        assert archive.download.url == "https://example.com/archive.zip"
        assert archive.download.name == "test_archive.zip"

    def test_date_times_default_empty(self, mock_request_helper: object) -> None:
        data = {
            "id": 1,
            "name": "Test",
            "horizon": "daily",
            "archive_type": "data",
            "download": {
                "name": "test.zip",
                "url": "https://example.com/archive.zip",
            },
            "date": datetime(2024, 1, 15, 10, 0, 0),
            "date_times": [],
            "publication_date": [],
            "taxonomy_terms": [],
            "vocabularies": [],
            "raw": {},
            "_request_helper": mock_request_helper,
        }
        archive = Archive(**data)
        assert archive.date_times == []

    def test_separate_instances_have_separate_lists(
        self, mock_request_helper: object
    ) -> None:
        data1 = {
            "id": 1,
            "name": "Archive 1",
            "horizon": "daily",
            "archive_type": "data",
            "download": {
                "name": "archive1.zip",
                "url": "https://example.com/1.zip",
            },
            "date": datetime(2024, 1, 15, 10, 0, 0),
            "date_times": [],
            "publication_date": [],
            "taxonomy_terms": [],
            "vocabularies": [],
            "raw": {},
            "_request_helper": mock_request_helper,
        }
        data2 = {
            "id": 2,
            "name": "Archive 2",
            "horizon": "daily",
            "archive_type": "data",
            "download": {
                "name": "archive2.zip",
                "url": "https://example.com/2.zip",
            },
            "date": datetime(2024, 1, 16, 10, 0, 0),
            "date_times": [],
            "publication_date": [],
            "taxonomy_terms": [],
            "vocabularies": [],
            "raw": {},
            "_request_helper": mock_request_helper,
        }

        archive1 = Archive(**data1)
        archive2 = Archive(**data2)

        archive1.date_times.append(date(2024, 1, 15))
        archive2.date_times.append(date(2024, 1, 16))

        assert len(archive1.date_times) == 1
        assert len(archive2.date_times) == 1
        assert archive1.date_times[0] == date(2024, 1, 15)
        assert archive2.date_times[0] == date(2024, 1, 16)

    def test_taxonomy_terms(self, archive_data: dict[str, Any]) -> None:
        archive = Archive(**archive_data)
        assert len(archive.taxonomy_terms) == 1
        assert archive.taxonomy_terms[0].id_taxonomy_term == 1
        assert archive.taxonomy_terms[0].name == "energy"
        assert archive.taxonomy_terms[0].vocabulary_id == 1

    def test_vocabularies(self, archive_data: dict[str, Any]) -> None:
        archive = Archive(**archive_data)
        assert len(archive.vocabularies) == 1
        assert archive.vocabularies[0].id_vocabulary == 1
        assert archive.vocabularies[0].name == "power"

    def test_raw_attribute(self, archive_data: dict[str, Any]) -> None:
        archive = Archive(**archive_data)
        assert archive.raw == {"key": "value"}

    def test_download_file_calls_request_helper(
        self, archive_data: dict[str, Any], mocker: MockerFixture
    ) -> None:
        mock_request_helper = mocker.MagicMock()
        archive_data["_request_helper"] = mock_request_helper
        archive = Archive(**archive_data)

        mock_response = mocker.MagicMock()
        mock_response.content = b"test content"
        mock_request_helper.get_request.return_value = mock_response

        archive.download_file(path="/tmp", unzip=False)

        mock_request_helper.get_request.assert_called_once_with(
            "https://example.com/archive.zip"
        )
