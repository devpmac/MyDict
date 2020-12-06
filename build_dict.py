from language_dictionary import LanguageDictionary, WordDefinition

ld = LanguageDictionary.from_files("de", ["Data/dict_DE.txt"])

for word, definitions in ld.words.items():
    print(word, "\n", definitions[0])
    break

# lang_dict.print_lines_to_file("test.txt")
