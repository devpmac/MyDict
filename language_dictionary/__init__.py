SUPPORTED_LANGUAGES = {"pt", "de", "en"}
ARTICLES = {"de": {"der", "die", "das", "dem", "den", "des", "ein", "eine", "eins", "einer"},
            "en": {"the", "a", "an"},
            "pt": {"o", "a", "os", "as", "um", "uma", "uns", "umas"}}


# from language_dictionary.utils import read_lines_from_files, replace_odd_characters
from language_dictionary import utils
from language_dictionary.word import Word
from language_dictionary.language_dictionary import LanguageDictionary
