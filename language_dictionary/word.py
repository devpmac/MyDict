from typing import List, TypeVar, Optional
from language_dictionary import WordDefinition

TypeWord = TypeVar("Word", bound="Word")


class Word:
    def __init__(self, word: str, definitions: Optional[List[WordDefinition]] = None):
        self.word = word
        self.definitions = definitions
