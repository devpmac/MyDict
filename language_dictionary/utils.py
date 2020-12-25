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


replace_a = str.maketrans("áàâäãÁÀÂÄÃ", "aaaaaAAAAA", "")
replace_e = str.maketrans("éèêëÉÈÊË", "eeeeEEEE", "")
replace_i = str.maketrans("íìîïÍÌÎÏ", "iiiiiiii", "")
replace_o = str.maketrans("óòôöõÓÒÔÖÕ", "oooooOOOOO", "")
replace_u = str.maketrans("úùûüÚÙÛÜ", "uuuuUUUU", "")
replace_ss = str.maketrans({"ß": "ss"})
replace_pl = str.maketrans("ąćęłńóśźżĄĆĘŁŃÓŚŹŻ", "acelnoszzACELNOSZZ", "")
replace_misc = str.maketrans("çÇñÑ", "cCnN", "")
translation_tables = [replace_a, replace_e, replace_i, replace_o, replace_u, replace_ss, replace_pl, replace_misc]

def replace_odd_characters(text: str):
    new_text = text
    for table in translation_tables:
        new_text = new_text.translate(table)
    return new_text
