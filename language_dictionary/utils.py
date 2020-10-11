from typing import List

def read_lines_from_files(files: List[str]) -> set:
    """
    Returns a set with all the lines found in input files.

    Parameters:
    -----------
    files : list
            List of strings corresponding to the names of the files

    Returns:
            line_set
    """
    lines = set()

    for name in files:
        with open(name) as file:
            lines.update(file.readlines())

    return lines