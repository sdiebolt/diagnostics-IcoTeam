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
    """ Read ``data_hashes.txt`` file in `data_directory`, check hashes

    Parameters
    ----------
    data_directory : str
        Directory containing data and ``data_hashes.txt`` file.

    Returns
    -------
    None

    Raises
    ------
    ValueError:
        If hash value for any file is different from hash value recorded in
        ``data_hashes.txt`` file.
    """
    # Read lines from ``data_hashes.txt`` file.
    # Split into SHA1 hash and filename
    # Calculate actual hash for given filename.
    # If hash for filename is not the same as the one in the file, raise
    # ValueError
    # This is a placeholder, replace it to write your solution.
    raise NotImplementedError('This is just a template -- you are expected to code this.')


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
