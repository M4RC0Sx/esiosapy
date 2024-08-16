from pathlib import Path
from typing import Union
from zipfile import ZipFile


def recursive_unzip(
    zip_path: Union[str, Path], unzip_path: Union[str, Path], remove: bool = False
) -> None:
    zip_path, unzip_path = Path(zip_path), Path(unzip_path)

    with ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(unzip_path)

    for zip_subfile in unzip_path.rglob("*.zip"):
        nested_unzip_path = zip_subfile.parent / zip_subfile.stem
        with ZipFile(zip_subfile, "r") as zip_ref:
            zip_ref.extractall(nested_unzip_path)

        recursive_unzip(zip_subfile, nested_unzip_path, remove)

        if remove and zip_subfile.exists():
            zip_subfile.unlink()

    if remove and zip_path.exists():
        zip_path.unlink()
