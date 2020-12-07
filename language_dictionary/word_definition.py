from typing import List, TypeVar
import re


from language_dictionary import SUPPORTED_LANGUAGES


TypeWordDefinition = TypeVar("WordDefinition", bound="WordDefinition")


class WordDefinitionError(Exception):
    pass


class WordDefinition:
    WORD_TAGS = {"adj", "adv", "conj", "expr", "n", "pron", "prep", "f", "m", "nt", "pl", "v"}
    REMOVE_ARTICLES_DE = re.compile(r"(der )|(die )|(das )")
    # TODO: SPLIT WORD_KEYS IN OPTIONAL AND NECESSARY
    WORD_KEYS = ("word", "tags", "definition", "example")
    REGEX_WORD_AND_TAGS = re.compile(r"(.*)\s+\((.+)\)")

    def __init__(self, language: str, word: str, tags: str, definition: str, example: str = None):
        self.language = self.validate_language(language)
        self.tags = self.validate_tags(tags)

        self.word = self.standardize_word(word)

        self.definition = definition
        self.example = example

    def __repr__(self):
        """"""
        representation = f'WordDefinition(word="{self.word}", tags={self.tags}, definition="{self.definition}"'
        if self.example is not None:
            representation += f', example="{self.example}"'
        representation += ")"
        return representation

    def __str__(self):
        printable_string = f"{self.word} {self.format_tags()} - {self.definition}"
        if self.example is not None:
            printable_string += f" - {self.example}"
        return printable_string + "\n"

    def format_tags(self):
        return "(" + ", ".join(self.tags) + ")"

    @classmethod
    def from_line(cls, language: str, line: str, sep: str = "-") -> TypeWordDefinition:
        new_entry = {key: None for key in cls.WORD_KEYS}
        new_entry["language"] = language

        word_tags, *remaining_values = line.split(sep)

        regex_word_and_tags = cls.REGEX_WORD_AND_TAGS.search(word_tags)
        if regex_word_and_tags:
            word, tags = regex_word_and_tags.groups()
            new_entry["word"] = word
            new_entry["tags"] = tags.split(", ")
            remaining_keys = cls.WORD_KEYS[2:]

            for i, value in enumerate(remaining_values):
                if i >= len(remaining_keys):
                    break
                key = remaining_keys[i]
                new_entry[key] = value.strip()

        return WordDefinition(**new_entry)

    def standardize_word(self, word: str) -> str:
        word = word.strip().lower()
        if self.language == "de" and "n" in self.tags:
            word = self.REMOVE_ARTICLES_DE.sub("", word)
            word = word.strip().capitalize()
        return word

    def validate_tags(self, tags: List[str]) -> List[str]:
        return [tag for tag in tags if tag in self.WORD_TAGS]

    def validate_language(self, language: str) -> str:
        std_language = language.lower()
        if std_language in SUPPORTED_LANGUAGES:
            return std_language
        else:
            raise WordDefinitionError("Specified language is not supported")
