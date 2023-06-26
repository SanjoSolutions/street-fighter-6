import os.path

characters = next(os.walk('characters'))[1]
for character in characters:
    character_directory = 'characters/' + character

    moves_path = character_directory + '/moves.csv'

    if os.path.isfile(moves_path):
        with open(moves_path, encoding='utf-8') as file:
            content = file.read()
            lines = content.split('\n')
            lines = lines[1:]
            if lines[-1] == '':
                lines = lines[:-1]

            entries = [line.split(',') for line in lines]
            regular_moves = [
                {'name': entry[0], 'drive gauge': float(entry[1] or 0), 'super art gauge': int(entry[2] or 0), 'is normal': entry[3] == 'TRUE', 'damage': int(entry[4]), 'advantage on hit': int(entry[5]) if entry[5] != '' else None, 'startup': int(entry[6]) if entry[6] != '' else None}
                for entry in entries
            ]

            moves_on_counter = [{**move, 'name': move['name'] + ' (Counter)', 'advantage on hit': move['advantage on hit'] + 2 if move['advantage on hit'] else None} for move in regular_moves]

            moves_on_punish_counter = [{**move, 'name': move['name'] + ' (Counter)', 'advantage on hit': move['advantage on hit'] + 4 if move['advantage on hit'] else None} for move in regular_moves]

            first_moves = regular_moves + moves_on_counter + moves_on_punish_counter

            connecting_moves = []

            for move in first_moves:
                moves_that_can_be_connected_with_move = [move2 for move2 in regular_moves if isinstance(move2['startup'], int) and isinstance(move['advantage on hit'], int) and move2['startup'] <= move['advantage on hit']]
                for move2 in moves_that_can_be_connected_with_move:
                    connecting_moves.append((move['name'], move2['name']))

            content = 'From,To,Conditions\n' + '\n'.join(connecting_move[0] + ',' + connecting_move[1] + ',' for connecting_move in connecting_moves)

            with open(character_directory + '/generated_connecting_moves.csv', mode='w', encoding='utf-8') as output_file:
                output_file.write(content)
