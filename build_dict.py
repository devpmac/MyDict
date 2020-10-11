from language_dictionary import LanguageDictionary, DictionaryEntry

lang_dict = LanguageDictionary.from_files("pt", ["dict_PT.txt"])
t1 = list(lang_dict.entries_lines)[:2]

d1 = DictionaryEntry.from_line(t1[0], sep="-")


# lang_dict.print_lines_to_file("test.txt")