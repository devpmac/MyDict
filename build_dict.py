from language_dictionary import LanguageDictionary  # , WordDefinition

INPUT_FILE = "Data/dict_DE.txt"
OUTPUT_FILE = "Data/dict_DE.txt"

# ld = LanguageDictionary.from_files("de", ["Data/dict_DE.txt"])
ld = LanguageDictionary.from_files("de", [INPUT_FILE])

# for word in sorted(ld.words):
    # print(word)
#     break

w1, w2 = sorted(ld.words)[:2]

ld.print_lines_to_file(OUTPUT_FILE)
