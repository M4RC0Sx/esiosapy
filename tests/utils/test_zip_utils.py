from __future__ import annotations

import tempfile

from pathlib import Path
from typing import TYPE_CHECKING
from zipfile import ZipFile

import pytest

from esiosapy.utils.zip_utils import recursive_unzip


if TYPE_CHECKING:
    from collections.abc import Generator


class TestRecursiveUnzip:
    @pytest.fixture
    def temp_dir(self) -> Generator[Path, None, None]:
        with tempfile.TemporaryDirectory() as tmp:
            yield Path(tmp)

    def test_extract_single_file(self, temp_dir: Path) -> None:
        """Test extracting a zip file with a single file."""
        zip_path = temp_dir / "test.zip"
        unzip_path = temp_dir / "output"

        with ZipFile(zip_path, "w") as zf:
            zf.writestr("file.txt", "Hello, World!")

        recursive_unzip(zip_path, unzip_path)

        assert (unzip_path / "file.txt").exists()
        assert (unzip_path / "file.txt").read_text() == "Hello, World!"

    def test_extract_multiple_files(self, temp_dir: Path) -> None:
        """Test extracting a zip file with multiple files."""
        zip_path = temp_dir / "multi.zip"
        unzip_path = temp_dir / "output"

        with ZipFile(zip_path, "w") as zf:
            zf.writestr("file1.txt", "Content 1")
            zf.writestr("file2.txt", "Content 2")
            zf.writestr("subdir/file3.txt", "Content 3")

        recursive_unzip(zip_path, unzip_path)

        assert (unzip_path / "file1.txt").exists()
        assert (unzip_path / "file2.txt").exists()
        assert (unzip_path / "subdir" / "file3.txt").exists()

    def test_extract_nested_zip(self, temp_dir: Path) -> None:
        """Test extracting a zip file that contains another zip file."""
        inner_zip_path = temp_dir / "inner.zip"
        outer_zip_path = temp_dir / "outer.zip"
        unzip_path = temp_dir / "output"

        with ZipFile(inner_zip_path, "w") as zf:
            zf.writestr("nested.txt", "Nested content")

        with ZipFile(outer_zip_path, "w") as zf:
            zf.writestr("outer.txt", "Outer content")
            zf.write(inner_zip_path, "nested.zip")

        recursive_unzip(outer_zip_path, unzip_path)

        # Outer file should be extracted
        assert (unzip_path / "outer.txt").exists()
        # Nested zip content should be extracted (inner content)
        nested_dir = unzip_path / "nested"
        assert (nested_dir / "nested.txt").exists()

    def test_remove_zip_after_extraction(self, temp_dir: Path) -> None:
        """Test that zip file is removed when remove=True."""
        zip_path = temp_dir / "test.zip"
        unzip_path = temp_dir / "output"

        with ZipFile(zip_path, "w") as zf:
            zf.writestr("file.txt", "Content")

        recursive_unzip(zip_path, unzip_path, remove=True)

        assert not zip_path.exists()
        assert (unzip_path / "file.txt").exists()

    def test_preserve_zip_when_remove_false(self, temp_dir: Path) -> None:
        """Test that zip file is preserved when remove=False."""
        zip_path = temp_dir / "test.zip"
        unzip_path = temp_dir / "output"

        with ZipFile(zip_path, "w") as zf:
            zf.writestr("file.txt", "Content")

        recursive_unzip(zip_path, unzip_path, remove=False)

        assert zip_path.exists()
        assert (unzip_path / "file.txt").exists()

    def test_accepts_string_paths(self, temp_dir: Path) -> None:
        """Test that function accepts string paths instead of Path objects."""
        zip_path = str(temp_dir / "test.zip")
        unzip_path = str(temp_dir / "output")

        with ZipFile(zip_path, "w") as zf:
            zf.writestr("file.txt", "Content")

        recursive_unzip(zip_path, unzip_path)

        assert (Path(unzip_path) / "file.txt").exists()


class TestRecursiveUnzipExists:
    def test_function_exists(self) -> None:
        assert callable(recursive_unzip)
