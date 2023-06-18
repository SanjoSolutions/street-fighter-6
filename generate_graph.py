import re
import os

with open('ryu.csv', encoding='utf-8') as file:
    content = file.read()
    lines = content.split('\n')
    lines = lines[1:]
    content = '\n'.join(lines)
    content = re.sub('(.+?),(.+)', '"\\1" -> "\\2"', content)
    content = 'digraph {\n' + content + '\n}'

    with open('ryu.dot', mode='w', encoding='utf-8') as output_file:
        output_file.write(content)

    os.system('dot -Tsvg -o ryu.svg ryu.dot')
