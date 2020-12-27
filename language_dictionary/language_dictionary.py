from typing import List, TypeVar
from language_dictionary import utils, Word


TypeLanguageDictionary = TypeVar("TypeLanguageDictionary", bound="LanguageDictionary")


class LanguageDictionaryError(Exception):
    pass

class LanguageDictionary:
    POSSIBLE_SEP = {"\t", "|", "-"}

    def __init__(self, language: str, sep: str = None):
        self.language = language
        self.words = set()
        self.sep = sep if sep is not None else "\t"

    @classmethod
    def from_files(cls, language: str, files: List[str], sep: str = None) -> TypeLanguageDictionary:
        new_dict = LanguageDictionary(language=language, sep=sep)
        lines = cls.get_lines_from_files(files)
        new_dict.determine_sep(list(lines)[0])
        new_dict.get_words_from_lines(lines)
        return new_dict

    @classmethod
    def get_lines_from_files(cls, files: List[str]):
        lines = utils.read_lines_from_files(files)
        return cls.format_lines(lines)

    def determine_sep(self, line):
        if len(line.split(self.sep)) == len(Word.WORD_KEYS):
            return
        else:
            for sep in self.POSSIBLE_SEP.difference({self.sep}):
                if len(line.split(sep)) == len(Word.WORD_KEYS):
                    self.sep = sep
                    return
            raise LanguageDictionaryError(f"Unable to find appropriate separator for line:\n{line}")

    def get_known_word(self, word_to_check: Word):
        for known_word in self.words:
            if known_word == word_to_check:
                return known_word

    def append_word(self, new_word: Word):
        known_word = self.get_known_word(new_word)
        if not known_word:
            self.words.add(new_word)
        else:
            known_word.merge(new_word)

    def get_words_from_lines(self, lines: List[str]):
        for line in lines:
            word = self.get_word_from_line(line)
            self.append_word(word)

    def get_word_from_line(self, line: str) -> Word:
        if self.language != "de":
            line = line.lower()
        return Word.from_line(language=self.language, line=line, sep=self.sep)

    def print_lines_to_file(self, output_file: str):
        """
        Print dictionary entries to output file.
        Blank line separates different letters.
        """
        with open(output_file, "w") as file:
            # Dictionary starts with "A"
            initial = "A"
            for entry in sorted(self.words):
                if entry:
                    new_initial = entry.get_initial().upper()
                    if new_initial != initial:
                        file.write("\n")
                    file.write(str(entry))
                    initial = new_initial

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
