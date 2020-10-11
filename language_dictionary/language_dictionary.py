from typing import List, TypeVar
from language_dictionary import read_lines_from_files, Word


TypeLanguageDictionary = TypeVar("TypeLanguageDictionary", bound="LanguageDictionary")


class LanguageDictionary:
    def __init__(self, language: str, sep: str = "-"):
        self.language = language
        self.entries_lines = set()
        self.entries_dict = dict()
        self.sep = sep

    @classmethod
    def from_files(cls, language: str, files: List[str], sep: str = "-") -> TypeLanguageDictionary:
        new_dict = LanguageDictionary(language=language, sep=sep)
        new_dict.get_lines_from_files(files)
        new_dict.get_entries_from_lines()
        return new_dict

    def get_lines_from_files(self, files: List[str]):
        lines = read_lines_from_files(files)
        self.entries_lines = self.format_lines(lines)

    def get_entry_from_line(self, line: str) -> Word:
        return Word.from_line(line, sep=self.sep)

    def get_entries_from_lines(self):
        for line in self.entries_lines:
            entry = self.get_entry_from_line(line)
            if entry.word not in self.entries_dict:
                self.entries_dict[entry.word] = [entry]
            elif entry not in self.entries_dict[entry.word]:
                self.entries_dict[entry.word].append(entry)

    def print_lines_to_file(self, output_file: str):
        """
        Print dictionary entries to output file.
        Blank line separates different letters.
        """
        with open(output_file, "w") as file:
            # Dictionary starts with "A"
            initial = "A"
            for entry in sorted(self.entries_lines):
                if entry:
                    new_initial = entry[0].upper()
                    if new_initial != initial:
                        entry = "\n" + entry
                    file.write(entry)
                    initial = new_initial

            if not entry.endswith("\n"):
                file.write("\n")

    @classmethod
    def format_lines(cls, lines: set) -> set:
        """
        Returns set of valid dictionary entries from set of lines.
        """
        return {cls.format_line(line) for line in lines if cls.is_dict_entry(line)}

    @classmethod
    def is_dict_entry(cls, line: str) -> bool:
        """
        Check if line is a dictionary entry: starts with a letter.
        """
        return line[0].isalpha()

    @classmethod
    def format_line(cls, line: str) -> bool:
        """
        Ensure string ends with newline.
        """
        return line if line.endswith("\n") else line + "\n"
