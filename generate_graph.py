import re
import os

def deduplicate(entries):
    dictionary = dict()
    result_entries = list()
    for entry in entries:
        [from_, to] = entry
        if from_ not in dictionary or to not in dictionary[from_]:
            result_entries.append(entry)
            if from_ not in dictionary:
                dictionary[from_] = set()
            dictionary[from_].add(to)
    return result_entries


characters = next(os.walk('characters'))[1]
for character in characters:
    character_directory = 'characters/' + character
    with open(character_directory + '/connecting_moves.csv', encoding='utf-8') as file:
        content = file.read()
        lines = content.split('\n')
        lines = lines[1:]

        entries = [line.split(',') for line in lines]
        entries = deduplicate(entries)

        content = 'digraph {\n' + '\n'.join('"' + entry[0] + '" -> "' + entry[1] + '"' for entry in entries) + '\n}'

        with open(character_directory + '/connecting_moves.dot', mode='w', encoding='utf-8') as output_file:
            output_file.write(content)

        os.system('dot -Tsvg -o ' + character_directory + '/connecting_moves.svg ' + character_directory + '/connecting_moves.dot')
