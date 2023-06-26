import os
import os.path
import re
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
                (entry[0], {'drive gauge': float(entry[1] or 0), 'super art gauge': int(entry[2] or 0), 'is normal': entry[3] == 'TRUE', 'damage': int(entry[4])})
                for entry in entries)


        def can_continue_with_sonic_break(combo):
            return 'Solid Puncher' in combo and combo[-4:] != (
                'Sonic Break', 'Sonic Break', 'Sonic Break', 'Sonic Break')


        def can_continue_combo_with_move(combo, move: str):
            can_do = (continuation_move == 'Sonic Break' and can_continue_with_sonic_break(combo) or continuation_move != 'Sonic Break') \
                and has_enough_resources_for_move(move, combo) \
                and (not move.startswith('(After drive rush) ') or combo[-1] in {'Parry Drive Rush', 'Cancel Drive Rush'}) \
                and not (move == 'Burning Straight' and len(combo) >= 2 and combo[-2] == 'Burning Straight' and combo[-1] == 'Sonic Boom')

            if can_do:
                if move in {'Sonic Hurricane', 'Heavy Sonic Hurricane'} and len(combo) >= 1 and combo[-1] == 'Heavy Somersault Kick':
                    return len(combo) >= 2 and combo[-2] == 'Phantom Cutter'  # See combo trial Intermediate 10
                else:
                    return True
            else:
                return False


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
                return retrieve_move(move)['drive gauge']
            else:
                return 0


        def determine_move_super_art_usage(move):
            if move in moves:
                return retrieve_move(move)['super art gauge']
            else:
                return 0


        def calculate_damage(combo):
            multiplier = 1
            damage = 0
            previous_move = None
            i = 1
            for move in combo:
                if i >= 3 and previous_move in {'Parry Drive Rush', 'Cancel Drive Rush'} and not ('Parry Drive Rush' in combo[1:] or 'Cancel Drive Rush' in combo[1:]):
                    multiplier = max(multiplier - 0.15, 0.1)
                elif i >= 2 and is_normal_move(move) and multiplier > 0.1:
                    multiplier = max(multiplier - 0.1, 0.1)

                move_multiplier = max(multiplier, 0.5) if is_super_art(move) else multiplier
                damage += move_multiplier * retrieve_move(move)['damage']

                previous_move = move
                i += 1
            return damage


        def is_normal_move(move):
            return retrieve_move(move)['is normal']


        def retrieve_move(move):
            if move in moves:
                return moves[move]
            else:
                match = re.match('^(?:\\(After drive rush\\) )?(?:(?:Light|Medium|Heavy) )?(.+?)(?: \\((?:Punish Counter|Counter|Block|Perfect)\\))?$', move)
                if match:
                    alternative_move_name = match.group(1)
                    if alternative_move_name in moves:
                        return moves[alternative_move_name]
            return None

        def is_super_art(move):
            return move in moves and retrieve_move(move)['super art gauge'] > 0


        with open(character_directory + '/connecting_moves.csv',
                  encoding='utf-8') as file:
            content = file.read()
            lines = content.split('\n')
            lines = lines[1:]

            entries = [line.split(',') for line in lines]
            entries = deduplicate(entries)

            from_to = dict()
            for entry in entries:
                from_ = entry[0]
                to = entry[1]
                if from_ not in from_to:
                    from_to[from_] = set()
                from_to[from_].add(to)

            combos = []
            combos_to_further_extend_after = []

            starting_moves = [move for move in from_to.keys() if move != 'Sonic Break' and not move.startswith('(After drive rush) ')]
            for starting_move in starting_moves:
                continuation_moves = from_to[starting_move]
                for continuation_move in continuation_moves:
                    if can_continue_combo_with_move((starting_move,), continuation_move):
                        combo = (starting_move, continuation_move)
                        combos.append(combo)
                        combos_to_further_extend_after.append(combo)

            combos_to_extend = combos_to_further_extend_after

            while len(combos_to_extend) >= 1:
                combos_to_further_extend_after = []
                for combo in combos_to_extend:
                    has_used_maximum_drive_gauge = determine_drive_gauge_usage(combo) >= 6
                    has_used_maximum_super_art_gauge = determine_super_art_gauge_usage(combo) == 3
                    if not has_used_maximum_drive_gauge or not has_used_maximum_super_art_gauge:
                        last_move = combo[-1]
                        if last_move in from_to:
                            continuation_moves = from_to[last_move]
                            for continuation_move in continuation_moves:
                                if can_continue_combo_with_move(combo, continuation_move):
                                    new_combo = combo + (continuation_move,)
                                    combos.append(new_combo)
                                    if calculate_damage(combo) < 11000:
                                        combos_to_further_extend_after.append(new_combo)
                combos_to_extend = combos_to_further_extend_after

            combos_with_metadata = [{'combo': combo, 'damage': calculate_damage(combo)} for combo in combos]
            combos_with_metadata.sort(key = lambda combo_with_metadata: combo_with_metadata['damage'], reverse = True)

            content = '\n'.join(' > '.join(combo_with_metadata['combo']) + ' (~' + str(combo_with_metadata['damage']) + ' damage, ' + str(determine_super_art_gauge_usage(combo_with_metadata['combo'])) + ' super art gauge, ' + str(determine_drive_gauge_usage(combo_with_metadata['combo'])) + ' drive gauge)' for combo_with_metadata in combos_with_metadata)

            with open(character_directory + '/combos.txt', mode='w',
                      encoding='utf-8') as output_file:
                output_file.write(content)

            selected_combos = [combo_with_metadata for combo_with_metadata in combos_with_metadata if 'Crossfire Somersault' not in combo_with_metadata['combo'] and 'Sonic Hurricane' not in combo_with_metadata['combo'] and not any(('Sonic Boom', 'Burning Straight') == combo_with_metadata['combo'][index:index+2] for index in range(0, len(combo_with_metadata['combo'])))]

            content = '\n'.join(' > '.join(combo_with_metadata['combo']) + ' (~' + str(combo_with_metadata['damage']) + ' damage, ' + str(determine_super_art_gauge_usage(combo_with_metadata['combo'])) + ' super art gauge, ' + str(determine_drive_gauge_usage(combo_with_metadata['combo'])) + ' drive gauge)' for combo_with_metadata in selected_combos)

            with open(character_directory + '/selected_combos.txt', mode='w',
                      encoding='utf-8') as output_file:
                output_file.write(content)
