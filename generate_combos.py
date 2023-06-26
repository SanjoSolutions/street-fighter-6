import os
import os.path
from functions import deduplicate

characters = next(os.walk('characters'))[1]
for character in characters:
    character_directory = 'characters/' + character

    moves_path = character_directory + '/moves.csv'

    if os.path.isfile(moves_path):
        with open(moves_path,
                  encoding='utf-8') as file:
            content = file.read()
            lines = content.split('\n')
            lines = lines[1:]
            if lines[-1] == '':
                lines = lines[:-1]

            entries = [line.split(',') for line in lines]
            moves = dict(
                (entry[0], {'drive gauge': float(entry[1]), 'super art gauge': int(entry[2])})
                for entry in entries)


        def can_continue_with_sonic_break(combo):
            return 'Solid Puncher' in combo and combo[-4:] != (
                'Sonic Break', 'Sonic Break', 'Sonic Break', 'Sonic Break')


        def can_continue_combo_with_move(combo, move: str):
            return (continuation_move == 'Sonic Break' and can_continue_with_sonic_break(combo) or continuation_move != 'Sonic Break') and has_enough_resources_for_move(move, combo) and (not move.startswith('(After drive rush) ') or combo[-1] in {'Parry Drive Rush', 'Cancel Drive Rush'})


        def has_enough_resources_for_move(move, combo):
            combo_drive_gauge_usage = determine_drive_gauge_usage(combo)
            combo_super_art_gauge_usage = determine_super_art_gauge_usage(combo)
            move_drive_gauge_required = determine_move_drive_gauge_usage(move)
            move_super_art_required = determine_move_super_art_usage(move)
            return combo_super_art_gauge_usage + move_super_art_required <= 3 and (
                    combo_drive_gauge_usage < 6 or move_drive_gauge_required == 0)


        def determine_drive_gauge_usage(combo):
            return sum(determine_move_drive_gauge_usage(move) for move in combo)


        def determine_super_art_gauge_usage(combo):
            return sum(determine_move_super_art_usage(move) for move in combo)


        def determine_move_drive_gauge_usage(move):
            if move in moves:
                return moves[move]['drive gauge']
            else:
                return 0


        def determine_move_super_art_usage(move):
            if move in moves:
                return moves[move]['super art gauge']
            else:
                return 0


        def calculate_damage(combo):
            multiplier = 1
            damage = 0
            previous_move = None
            for move in combo:
                if is_normal_move(move) and previous_move is not None:
                    multiplier -= 0.1

                damage = multiplier * move['damage']

                previous_move = move
            return damage


        def is_normal_move(move):
            return moves[move]['is normal']


        with open(character_directory + '/connecting_moves.csv',
                  encoding='utf-8') as file:
            content = file.read()
            lines = content.split('\n')
            lines = lines[1:]

            entries = [line.split(',') for line in lines]
            entries = deduplicate(entries)

            from_to = dict()
            for entry in entries:
                [from_, to] = entry
                if from_ not in from_to:
                    from_to[from_] = set()
                from_to[from_].add(to)

            combos = []
            new_combos = []

            starting_moves = [move for move in from_to.keys() if move != 'Sonic Break' and not move.startswith('(After drive rush) ')]
            for starting_move in starting_moves:
                continuation_moves = from_to[starting_move]
                for continuation_move in continuation_moves:
                    if can_continue_combo_with_move((starting_move,), continuation_move):
                        combo = (starting_move, continuation_move)
                        combos.append(combo)
                        new_combos.append(combo)

            combos_to_continue = new_combos

            while len(combos_to_continue) >= 1:
                new_combos = []
                for combo in combos_to_continue:
                    has_used_maximum_drive_gauge = determine_drive_gauge_usage(
                        combo) >= 6
                    has_used_maximum_super_art_gauge = determine_super_art_gauge_usage(
                        combo) == 3
                    if not has_used_maximum_drive_gauge or not has_used_maximum_super_art_gauge:
                        last_move = combo[-1]
                        if last_move in from_to:
                            continuation_moves = from_to[last_move]
                            for continuation_move in continuation_moves:
                                if can_continue_combo_with_move(combo, continuation_move):
                                    new_combo = combo + (continuation_move,)
                                    combos.append(new_combo)
                                    new_combos.append(new_combo)
                combos_to_continue = new_combos

            content = '\n'.join(' > '.join(combo) for combo in combos)

            with open(character_directory + '/combos.txt', mode='w',
                      encoding='utf-8') as output_file:
                output_file.write(content)
