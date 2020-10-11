from typing import List, TypeVar
from language_dictionary import PARTS_OF_SPEECH


DE = TypeVar("DE", bound="DictionaryEntry")


class DictionaryEntry(dict):
    # dict_values = ["meaning", "pos", "example"]
    def __init__(self, word: str, meaning: str, pos: str = None, example: str = None):
        super().__init__(meaning=meaning, pos=pos, example=example)
        self.word = word

    @classmethod
    def from_line(cls, line: str, sep: str = "-") -> DE:
        # word, meaning, pos, example = None, None, None, None
        entry = [None, None, None, None]

        values = line.split(sep)
        for i, v in enumerate(values):
            if i > 3:
                break
            entry[i] = v.strip()

        word, meaning, pos, example = cls.validate_entry(entry)
        new_entry = DictionaryEntry(word, meaning=meaning, pos=pos, example=example)
        return new_entry

    @classmethod
    def validate_entry(cls, entry: List) -> List:
        valid_entry = []
        validation_functions = [
            cls.validate_word,
            cls.validate_meaning,
            cls.validate_pos,
            cls.validate_example,
        ]
        for i, val in enumerate(validation_functions):
            valid_entry.append(val(entry[i]))
        return valid_entry

    @classmethod
    def validate_word(cls, word: str):
        return word

    @classmethod
    def validate_meaning(cls, meaning: str):
        return meaning

    @classmethod
    def validate_pos(cls, pos: str) -> str:
        return pos if pos in PARTS_OF_SPEECH else None

    @classmethod
    def validate_example(cls, example: str):
        return example