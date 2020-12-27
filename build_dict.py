from language_dictionary import LanguageDictionary  # , WordDefinition

# ld = LanguageDictionary.from_files("de", ["Data/dict_DE.txt"])
ld = LanguageDictionary.from_files("de", ["Data/test.txt"])

# for word in sorted(ld.words):
    # print(word)
#     break

w1, w2 = sorted(ld.words)[:2]

ld.print_lines_to_file("Data/dict_DE.txt")
