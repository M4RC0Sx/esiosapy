from pathlib import Path
from typing import Union
from zipfile import ZipFile


def recursive_unzip(
    zip_path: Union[str, Path], unzip_path: Union[str, Path], remove: bool = False
) -> None:
    """
    Recursively unzips a ZIP file and all nested ZIP files
    within it to a specified directory.

    This function extracts the contents of the provided ZIP file to the specified
    directory. If any ZIP files are found within the extracted contents, it will
    recursively extract them into their respective directories. Optionally, it can
    also delete the original ZIP files after extraction.

    :param zip_path: The path to the ZIP file to be unzipped.
                     This can be a string or a Path object.
    :type zip_path: Union[str, Path]
    :param unzip_path: The directory where the contents of the ZIP file
                       should be extracted. This can be a string or a Path object.
    :type unzip_path: Union[str, Path]
    :param remove: If set to True, the original ZIP files will be deleted
                   after extraction, including nested ZIP files. Defaults to False.
    :type remove: bool, optional

    :return: None
    """
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
