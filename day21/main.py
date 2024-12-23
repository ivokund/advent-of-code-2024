import unittest
from collections import namedtuple
from typing import Text

test_data = """029A
980A
179A
456A
379A"""

real_data = """593A
508A
386A
459A
246A"""

Key = namedtuple("Point", ["x", "y"])

MoveLabels = {
    (1, 0): '>',
    (-1, 0): '<',
    (0, 1): 'v',
    (0, -1): '^',
}

MoveDeltas = {
    '>': (1, 0),
    '<': (-1, 0),
    'v': (0, 1),
    '^': (0, -1),
}

# +---+---+---+
# | 7 | 8 | 9 |
# +---+---+---+
# | 4 | 5 | 6 |
# +---+---+---+
# | 1 | 2 | 3 |
# +---+---+---+
#     | 0 | A |
#     +---+---+
NumericKeys = {
    1: Key(0, 2),
    2: Key(1, 2),
    3: Key(2, 2),
    4: Key(0, 1),
    5: Key(1, 1),
    6: Key(2, 1),
    7: Key(0, 0),
    8: Key(1, 0),
    9: Key(2, 0),
    0: Key(1, 3),
    'A': Key(2, 3),
    'BLANK': Key(0, 3),
}
#     +---+---+
#     | ^ | A |
# +---+---+---+
# | < | v | > |
# +---+---+---+

DirectionalKeys = {
    '<': Key(0, 1),
    'v': Key(1, 1),
    '>': Key(2, 1),
    '^': Key(1, 0),
    'A': Key(2, 0),
    'BLANK': Key(0, 0),
}
class Keypad:
    def __init__(self, keys):
        self.keys = keys
        for val, coords in keys.items():
            if val == 'BLANK':
                # print(f'  Setting BLANK to {coords}')
                self.blank_pos = coords
            elif val == 'A':
                # print(f'  Setting A to {coords}')
                self.a_pos = coords

    # def get_paths_str(self, start, end):
    #     paths = self.get_all_paths(start, end)
    #     return ["".join([MoveLabels[move] for move in path]) for path in paths]

    def get_all_paths(self, start, end):
        from_coord = self.keys[start]
        to_coords = self.keys[end]
        dx = to_coords.x - from_coord.x
        dy = to_coords.y - from_coord.y

        step_x = dx // abs(dx) if dx != 0 else 0
        step_y = dy // abs(dy) if dy != 0 else 0

        move_x = (step_x, 0)
        move_y = (0, step_y)

        final_paths = set([])
        paths_queue = [([], from_coord)]
        while paths_queue:
            path, my_pos = paths_queue.pop(0)
            if my_pos == to_coords:
                final_paths.add(''.join([MoveLabels[move] for move in path]))
            elif my_pos == self.blank_pos:
                continue
            else:
                if my_pos.x != to_coords.x:
                    new_pos = Key(my_pos.x + step_x, my_pos.y)
                    paths_queue.append((path + [move_x], new_pos))
                if my_pos.y != to_coords.y:
                    new_pos = Key(my_pos.x, my_pos.y + step_y)
                    paths_queue.append((path + [move_y], new_pos))
        # print(f"  Generated paths:")
        # for idx, path in enumerate(final_paths):
        #     print(f"  Path {idx+1}: {path}")
        return final_paths

    def get_paths_for_key_sequence(self, sequence: Text):
        # print(f"Getting paths for sequence: {sequence}")
        paths_to_prepend = {''}
        start = 'A'
        for key in list(sequence):
            # print(f"  - moving from {start} to {key}")
            paths = self.get_all_paths(start, key)
            # print(f"  - received paths: {paths}")
            start = key
            new_paths = []
            for path in paths:
                for prev_path in paths_to_prepend:
                    new_paths.append(prev_path + path + 'A')
            paths_to_prepend = new_paths
            # print(f"  - new paths to prepend: {paths_to_prepend}")

        return paths_to_prepend


class Day21(unittest.TestCase):
    def test_numeric(self):
        # +---+---+---+
        # | 7 | 8 | 9 |
        # +---+---+---+
        # | 4 | 5 | 6 |
        # +---+---+---+
        # | 1 | 2 | 3 |
        # +---+---+---+
        #     | 0 | A |
        #     +---+---+
        pad = Keypad(NumericKeys)
        self.assertEqual({'<'}, pad.get_all_paths('A', 0))
        self.assertEqual({'^'}, pad.get_all_paths('A', 3))
        self.assertEqual({'^^^'}, pad.get_all_paths('A', 9))
        self.assertEqual({'<^<^^',
                          '<^^<^',
                          '<^^^<',
                          '^<<^^',
                          '^<^<^',
                          '^<^^<',
                          '^^<<^',
                          '^^<^<',
                          '^^^<<'}, pad.get_all_paths('A', 7))
        self.assertEqual({'<^<', '^<<'}, pad.get_all_paths('A', 1))

        pad = Keypad(NumericKeys)
        self.assertEqual({'>>vvv',
                          '>v>vv',
                          '>vv>v',
                          '>vvv>',
                          'v>>vv',
                          'v>v>v',
                          'v>vv>',
                          'vv>>v',
                          'vv>v>'}, pad.get_all_paths(7, 'A'))

    def test_directional(self):
        #     +---+---+
        #     | ^ | A |
        # +---+---+---+
        # | < | v | > |
        # +---+---+---+
        pad = Keypad(DirectionalKeys)
        self.assertEqual({'v'}, pad.get_all_paths('A', '>'))
        self.assertEqual({'<v<', 'v<<'}, pad.get_all_paths('A', '<'))

    def test_move_sequence(self):
        pad = Keypad(DirectionalKeys)
        new_steps = pad.get_paths_for_key_sequence('vA')
        self.assertEqual({'v<A^>A', 'v<A>^A', '<vA^>A', '<vA>^A'}, new_steps)


    def test_part1(self):
        self.assertEqual(126384, part1(test_data))
        self.assertEqual(157892, part1(real_data))


def part1(text):
    codes = [[int(num) if num != 'A' else 'A' for num in list(line)] for line in text.split("\n")]

    numeric_pad = Keypad(NumericKeys)
    directional_pad_1 = Keypad(DirectionalKeys)
    directional_pad_2 = Keypad(DirectionalKeys)

    def discard_longer_paths(paths):
        different_lengths = set([])
        for sequence in paths:
            different_lengths.add(len(sequence))
        min_l, max_l = min(list(different_lengths)), max(list(different_lengths))

        paths_with_min_length = set([path for path in paths if len(path) == min_l])
        return paths_with_min_length, min_l

    def get_min_sequence_length(code):
        print("Code:", code)
        robot_1_paths = numeric_pad.get_paths_for_key_sequence(code)
        prev_paths, r_min = discard_longer_paths(robot_1_paths)

        robot_count = 2

        for robot_num in range(0, robot_count):
            print("Robot", robot_num)
            robot_paths = set()
            for robot_path in prev_paths:
                robot_paths.update(directional_pad_1.get_paths_for_key_sequence(robot_path))

            prev_paths, r_min = discard_longer_paths(robot_paths)

        return r_min

    def get_complexity(code):
        return get_min_sequence_length(code) * int("".join([str(num) for num in code if num != 'A']))

    return sum([get_complexity(code) for code in codes])
