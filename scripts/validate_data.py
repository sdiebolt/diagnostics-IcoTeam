""" Python script to validate data

Run as:

    python3 scripts/validata_data.py data
"""

from pathlib import Path
import sys
from hashlib import sha1

def file_hash(filename):
    """ Get byte contents of file `filename`, return SHA1 hash

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
    TypeError :
        If filename cannot be casted to pathlib.Path
    ValueError :
        If filename returns False with ``filename.is_file()``
    """
    # Try filename as Path
    try:
        filename = Path(filename)
    except TypeError:
        raise TypeError(
            "filename argument must be a pathlib.Path (or a type that supports"
            " casting to pathlib.Path, such as string)."
        )
    
    # Get absolute filename, expand ~user formats and resolving symlinks or relative paths
    filename = filename.expanduser().resolve()

    # Check if file exists
    if not filename.is_file():
        raise ValueError(f"File not found: {filename}.")

    # Open the file, read contents as bytes.
    byte_contents = filename.read_bytes()

    # Calculate, return SHA1 has on the bytes from the file.
    return sha1(byte_contents).hexdigest()


def validate_data(data_directory):
    """ Read ``hash_list.txt`` or ``data_hashes.txt`` file in from `group-*` directory in `data_directory`,
    then check hashes. It will check all groups.

    Parameters
    ----------
    data_directory : str
        Directory containing data and `group-*` directory where ``hash_list.txt`` file is.

    Returns
    -------
    None

    Raises
    ------
    TypeError : 
        If `data_directory` cannot be casted to pathlib.Path
    ValueError :
        If `data_directory` returns False to `data_directory.is_dir()`
    ValueError :
        If there is no ``hash_list.txt`` or ``data_hashes.txt`` file inside the group directories.
    ValueError:
        If hash value for any file is different from hash value recorded in
        ``hash_list.txt`` file.
    """
    # Try data_directory as Path
    try:
        data_directory = Path(data_directory)
    except TypeError:
        raise TypeError(
            "data_directory argument must be a pathlib.Path (or a type that supports"
            " casting to pathlib.Path, such as string)."
        )

    # Get absolute filename, expand ~user formats and resolving symlinks or relative paths
    data_directory = data_directory.expanduser().resolve()

    # Check if directory exists
    if not data_directory.is_dir():
        raise ValueError(f"Directory not found: {data_directory}.")
    
    # Get hash list using glob to potentially validate more than one group at a time
    hash_paths = list(data_directory.glob("group-*/hash_list.txt"))
    # Get either `hash_list.txt` or `data_hashes.txt`
    hash_paths += list(data_directory.glob("group-*/data_hashes.txt"))

    # Check if any hash file exist
    if not hash_paths:
        raise ValueError(
            "No `hash_list.txt` or `data_hashes.txt` file was found in"
            f" {data_directory / 'group-*'}."
        )

    for hash_path in hash_paths:
        # Read lines from ``data_hashes.txt`` file.
        hashes_lines = hash_path.read_text().splitlines()
        for line in hashes_lines:
            # Split into SHA1 hash and filename
            expected_hash, filename = line.split()

            # Calculate actual hash for given filename.
            actual_hash = file_hash(data_directory / filename)

            # If hash for filename is not the same as the one in the file, raise
            # ValueError
            if not actual_hash == expected_hash:
                raise ValueError(
                    f"Hashes were not validated. File {filename} expected hash was {expected_hash} and"
                    f" actual hash is {actual_hash}."
                )


def main():
    # This function (main) called when this file run as a script.
    #
    # Get the data directory from the command line arguments
    if len(sys.argv) < 2:
        raise RuntimeError("Please give data directory on "
                           "command line")
    data_directory = sys.argv[1]
    # Call function to validate data in data directory
    validate_data(data_directory)


if __name__ == '__main__':
    # Python is running this file as a script, not importing it.
    main()
