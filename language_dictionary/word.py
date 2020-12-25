from typing import List, TypeVar
import re


from language_dictionary import SUPPORTED_LANGUAGES, ARTICLES, utils


TypeWord = TypeVar("Word", bound="Word")


class WordError(Exception):
    pass


class Word:
    WORD_TAGS = {"adj", "adv", "conj", "expr", "n", "pron", "prep", "f", "m", "nt", "pl", "v"}
    WORD_KEYS = ("word", "tags", "meanings", "examples", "other")
    LINE_SEP = "<br>"

    def __init__(self, language: str, word: str, tags: List[str], meanings: str, examples: str = None, other: str = None):
        self.language = self.validate_language(language)
        self.ARTICLES = ARTICLES[self.language]

        self.tags = self.validate_tags(tags)

        self.word = self.standardize_word(word)

        self.meanings = meanings
        self.examples = examples

        self.other = other

    def __repr__(self):
        """"""
        representation = f'Word(word="{self.word}", tags={self.tags}, meanings="{self.meanings}"'
        if self.examples is not None:
            representation += f', examples="{self.examples}"'
        if self.other is not None:
            representation += f', other="{self.other}"'
        representation += ")"
        return representation

    def __str__(self):
        printable_string = f"{self.word} | {self.format_tags()} | {self.format_meanings()} |"
        if self.examples is not None:
            printable_string += f" {self.format_examples()} |"
        else:
            printable_string += f" |"
        if self.other is not None:
            printable_string += f" {self.other}"
        return printable_string + "\n"

    def __lt__(self, other):
        if isinstance(other, Word):
            return self.get_initial() < other.get_initial()
        return NotImplemented

    def __eq__(self, other):
        if isinstance(other, Word):
            return self.language == other.language and self.word == other.word and self.tags == other.tags
        return NotImplemented

    def __hash__(self):
        return hash(self.language + self.word + " ".join(self.tags))

    @classmethod
    def process_tags(cls, tags: str):
        final_tags = set()
        for tag in tags.split(" "):
            if tag is not None:
                final_tags.update(tag.split("."))
        return list(final_tags)

    @classmethod
    def from_line(cls, language: str, line: str, sep: str = "|") -> TypeWord:
        new_entry = {key: None for key in cls.WORD_KEYS}
        new_entry["language"] = language

        word, tags, *remaining_values = line.split(sep)

        new_entry["word"] = word.strip()
        new_entry["tags"] = cls.process_tags(tags)

        remaining_keys = cls.WORD_KEYS[2:]
        for i, value in enumerate(remaining_values):
            if i >= len(remaining_keys):
                break
            value = value.strip()
            if not value:
                value = None
            else:
                value = [v.strip() for v in value.split(cls.LINE_SEP)]
            key = remaining_keys[i]
            new_entry[key] = value

        return Word(**new_entry)

    # Standardize values to store as attributes
    def standardize_word(self, word: str) -> str:
        word = word.strip()
        if self.language != "de":
            word = word.lower()

        elif "n" in self.tags:
            standardized = []
            for part in word.split(" "):
                if part not in self.ARTICLES:
                    part.capitalize()
                standardized.append(part)
            word = " ".join(standardized)

        elif "expr" not in self.tags:
            word = word.lower()

        return word

    def validate_tags(self, tags: List[str]) -> List[str]:
        return [tag for tag in tags if tag in self.WORD_TAGS]

    def validate_language(self, language: str) -> str:
        std_language = language.lower()
        if std_language in SUPPORTED_LANGUAGES:
            return std_language
        else:
            raise WordError("Specified language is not supported")

    # Format for string output
    def format_tags(self):
        if any(tag in {"f", "m", "nt", "pl"} for tag in self.tags):
            if "n" not in self.tags:
                raise WordError("Only nouns require gender and number tags.")
            output = []
            for tag in self.tags:
                if tag in {"f", "m", "nt", "pl"}:
                    output.append(f"n.{tag}")
                elif tag != "n":
                    output.append(tag)
            return " ".join(output)
        return " ".join(self.tags)

    def format_meanings(self):
        return self.LINE_SEP.join(self.meanings)

    def format_examples(self):
        return self.LINE_SEP.join(self.examples)

    def format_other(self):
        return self.LINE_SEP.join(self.other)

    # Word functionality
    def append_to_attr(self, attr: str, new_value: str):
        for new in new_value.split(self.LINE_SEP):
            new = new.strip()
            if new and new not in getattr(self, attr):
                new_val = getattr(self, attr).append(new)
                setattr(self, attr, new_val)

    def add_meaning(self, new_meaning: str):
        self.append_to_attr("meanings", new_meaning)

    def add_example(self, new_example: str):
        self.append_to_attr("examples", new_example)

    def add_other(self, new_other: str):
        self.append_to_attr("other", new_other)

    def merge(self, other):
        if self == other:
            for attr in {"meanings", "examples", "other"}:
                self.append_to_attr(attr, getattr(other, attr))

    # Other
    def get_initial(self):
        word = utils.replace_odd_characters(self.word)
        split_word = word.split(" ")
        initial = None
        for part in split_word:
            part = part.strip()
            if part.lower() not in self.ARTICLES and part[0].isalpha():
                initial = part[0]
                return initial
        if not initial:
            raise WordError(f"Unable to determine the initial for '{self.word}'.")
