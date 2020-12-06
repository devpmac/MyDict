from typing import List, TypeVar
from language_dictionary import read_lines_from_files, Word, WordDefinition


TypeLanguageDictionary = TypeVar("TypeLanguageDictionary", bound="LanguageDictionary")


class LanguageDictionary:
    def __init__(self, language: str, sep: str = "-"):
        self.language = language
        self.words = dict()
        self.sep = sep

    @classmethod
    def from_files(cls, language: str, files: List[str], sep: str = "-") -> TypeLanguageDictionary:
        new_dict = LanguageDictionary(language=language, sep=sep)
        lines = cls.get_lines_from_files(files)
        new_dict.get_entries_from_lines(lines)
        return new_dict

    @classmethod
    def get_lines_from_files(cls, files: List[str]):
        lines = read_lines_from_files(files)
        return cls.format_lines(lines)

    def get_definition_from_line(self, line: str) -> WordDefinition:
        if self.language != "de":
            line = line.lower()
        return WordDefinition.from_line(language=self.language, line=line, sep=self.sep)

    def append_definition(self, definition: WordDefinition):
        if definition not in self.words:
            self.words[definition.word] = [definition]
        else:
            self.words[definition.word].append(definition)

    def get_entries_from_lines(self, lines: List[str]):
        for line in lines:
            definition = self.get_definition_from_line(line)
            self.append_definition(definition)

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
