""" Python script to validate data

Run as:

    python3 scripts/validate_data.py
"""

from pathlib import Path
import sys
from hashlib import sha1


def file_hash(filename):
    """Get byte contents of file `filename`, return SHA1 hash

    Parameters
    ----------
    filename : str
        Name of file to read

    Returns
    -------
    hash : str
        SHA1 hexadecimal hash string for contents of `filename`.

    Raises
    -------
    TypeError
        If filename cannot be casted to pathlib.Path
    ValueError
        If filename returns False with ``filename.is_file()``
    """
    try:
        filename = Path(filename)
    except TypeError:
        raise TypeError(
            "filename argument must be a pathlib.Path (or a type that supports"
            " casting to pathlib.Path, such as string)."
        )

    # Python generally does not understand ~ and symlinks.
    filename = filename.expanduser().resolve()

    if not filename.is_file():
        raise ValueError(f"File not found: {filename}.")

    byte_contents = filename.read_bytes()

    return sha1(byte_contents).hexdigest()


def validate_data(data_directory):
    """Read ``hash_list.txt`` from `data_directory`, then check hashes.

    Parameters
    ----------
    data_directory : str
        Directory containing data and ``hash_list.txt``.

    Returns
    -------
    None

    Raises
    ------
    TypeError
        If `data_directory` cannot be casted to pathlib.Path
    ValueError
        If `data_directory` or `hash_list.txt` is not found.
    RuntimeError
        If any file's hash conflicts with those recorded in `hash_list.txt`.
    """
    try:
        data_directory = Path(data_directory)
    except TypeError:
        raise TypeError(
            "'data_directory' argument must be a pathlib.Path (or a type that supports"
            " casting to pathlib.Path, such as string)."
        )

    # Python generally does not understand ~ and symlinks.
    data_directory = data_directory.expanduser().resolve()

    if not data_directory.is_dir():
        raise ValueError(f"Directory not found: {data_directory}.")

    hash_path = data_directory / "hash_list.txt"

    if not hash_path.is_file():
        raise ValueError(f"File not found: {hash_path}.")

    hashes_lines = hash_path.read_text().splitlines()
    for line in hashes_lines:
        expected_hash, filename = line.split()

        actual_hash = file_hash(data_directory.parent / filename)

        if not actual_hash == expected_hash:
            raise RuntimeError(
                f"Hash conflict detected for file {filename}. Expected hash is " 
                f" {expected_hash}, computed hash is {actual_hash}."
            )


def main():
    """Main function called when this file is run as a script."""
    group_directory = Path(__file__).parent.parent / "data"
    groups = list(group_directory.glob("group-??"))
    if len(groups) == 0:
        raise RuntimeError(
            "No group directory in data directory: "
            "have you downloaded and unpacked the data?"
        )

    if len(groups) > 1:
        raise RuntimeError("Too many group directories in data directory")

    validate_data(groups[0])


if __name__ == "__main__":
    main()
