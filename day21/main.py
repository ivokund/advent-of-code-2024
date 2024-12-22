import unittest
from collections import namedtuple
from typing import Tuple, List

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
# ^A^^<<A>>AvvvA
#   < ?
# <A>A <AAv<AA>>^AvAA^Av<AAA^>A
#      v<<A ???
# <v<A>>^AvA^A <vA<AA>>^AAvA<^A>AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A -- correct
# v<<A>>^AvA^A v<<A>>^AAv<A<A>>^AAvAA^<A>Av<A^>AA<A>Av<A<A>>^AAA<Av>A^A
#     +---+---+
#     | ^ | A |
# +---+---+---+
# | < | v | > |
# +---+---+---+



# 375A: ^A^^<<Av>Avv>A length: 14
#       ^A^^<<A>vAvv>A
#
# 375A: <A>A<AAv<AA>>^Av<A>A^Av<AA>A^A length: 30
#       <A>A<AAv<AA>>^AvA<A^>Av<AA>A^A
#
# 375A: v<<A>>^AvA^Av<<A>>^AAv<A<A>>^AAvAA^<A>Av<A <A>>^AvA^A<A>Av<A<A>>^AAvA^A<A>A length: 74
#       v<<A>>^AvA^Av<<A>>^AAv<A<A>>^AAvAA^<A>Av<A ^>Av<<A>>^A<Av>A^Av<A<A>>^AAvA^A<A>A
DirectionalKeys = {
    '<': Key(0, 1),
    'v': Key(1, 1),
    '>': Key(2, 1),
    '^': Key(1, 0),
    'A': Key(2, 0),
    'BLANK': Key(0, 0),
}
class Keypad:
    def __init__(self, keys, start_key='A'):
        self.keys = keys
        for val, coords in keys.items():
            if val == start_key:
                print(f'  Setting start to {coords}')
                self.position = coords
            elif val == 'BLANK':
                print(f'  Setting BLANK to {coords}')
                self.blank_pos = coords

    def calculate_steps_to(self, to_key):
        to_coords = self.keys[to_key]
        dx = to_coords.x - self.position.x
        dy = to_coords.y - self.position.y

        my_pos = self.position
        moves = []

        step_x = dx // abs(dx) if dx != 0 else 0
        step_y = dy // abs(dy) if dy != 0 else 0

        print(f"=== moving from {my_pos} to {to_coords} with steps {step_x}, {step_y}")

        def move_x_axis():
            nonlocal my_pos
            if my_pos == to_coords or dx == 0:
                return
            while True:
                new_pos = Key(my_pos.x + step_x, my_pos.y)
                if new_pos == self.blank_pos:
                    break
                my_pos = new_pos
                moves.append((step_x, 0))
                if new_pos.x == to_coords.x:
                    break

        def move_y_axis():
            nonlocal my_pos
            if my_pos == to_coords or dy == 0:
                return
            while True:
                new_pos = Key(my_pos.x, my_pos.y + step_y)
                if new_pos == self.blank_pos:
                    break
                my_pos = new_pos
                moves.append((0, step_y))
                if new_pos.y == to_coords.y:
                    break

        x_first = my_pos.x == self.blank_pos.x
        print(f"  - x first: {x_first}")

        for _ in [1, 2]:
            if x_first:
                move_x_axis()
                move_y_axis()
            else:
                move_y_axis()
                move_x_axis()

        return moves
    
    def get_print_steps_to(self, to_key):
        moves = self.calculate_steps_to(to_key)
        moves_str = [MoveLabels[move] for move in moves] + ['A']
        return "".join(moves_str)

    def move(self, moves: List[Tuple[int, int]]):
        print(f"    == moving by steps {moves} ==")

        for dx, dy in moves:
            self.position = Key(self.position.x + dx, self.position.y + dy)
            print(f"  - moved to {self.position}")

        moves_str = "".join([MoveLabels[move] for move in moves] + ['A'])
        print(f"  - moves: {moves_str}")
        return moves_str

    def move_sequence(self, sequence):
        all_moves = ""
        for key in sequence:
            moves = self.calculate_steps_to(key)
            all_moves += self.move(moves)
        print(f"  - final position: {self.position}")
        return all_moves


class Day21(unittest.TestCase):
    @unittest.skip
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
        self.assertEqual('<A', pad.get_print_steps_to(0))
        self.assertEqual('^A', pad.get_print_steps_to(3))
        self.assertEqual('^^^A', pad.get_print_steps_to(9))
        self.assertEqual('^^^<<A', pad.get_print_steps_to(7))
        self.assertEqual('^<<A', pad.get_print_steps_to(1))

        pad = Keypad(NumericKeys, 7)
        self.assertEqual('>>vvvA', pad.get_print_steps_to('A'))

        pad = Keypad(NumericKeys, 3)
        self.assertEqual('asdasd', pad.get_print_steps_to(7))

    @unittest.skip
    def test_directional(self):
        #     +---+---+
        #     | ^ | A |
        # +---+---+---+
        # | < | v | > |
        # +---+---+---+
        pad = Keypad(DirectionalKeys)
        self.assertEqual('vA', pad.get_print_steps_to('>'))
        self.assertEqual('v<<A', pad.get_print_steps_to('<'))

    @unittest.skip
    def test_move_sequence(self):
        pad = Keypad(NumericKeys)
        steps = pad.move_sequence([0, 5])
        self.assertEqual('<A^^A', steps)


    def test_part1(self):
        self.assertEqual(126384, part1(test_data))
        # self.assertEqual(111, part1(real_data))


def part1(text):
    codes = [[int(num) if num != 'A' else 'A' for num in list(line)] for line in text.split("\n")]

    numeric_pad = Keypad(NumericKeys)
    directional_pad_1 = Keypad(DirectionalKeys)
    directional_pad_2 = Keypad(DirectionalKeys)

    def get_moves(code):
        robot_1_moves = numeric_pad.move_sequence(code)
        print("Robot 1 moves (numeric):", robot_1_moves)

        robot_2_moves = directional_pad_1.move_sequence(robot_1_moves)
        print("Robot 2 moves (directional):", robot_2_moves)

        robot_3_moves = directional_pad_2.move_sequence(robot_2_moves)
        print("Robot 3 moves (directional):", robot_3_moves)

        return robot_3_moves



    def get_complexity(moves, code):
        return len(moves), int("".join([str(num) for num in code if num != 'A']))

    codes = [[3, 7, 5, 'A']]
    m = get_moves(codes[0])
    print(get_complexity(m, codes[0]))

    complexities = [get_complexity(get_moves(code), code) for code in codes]
    #
    return (complexities)


# print("Part 1 test: ", part1(test_data))
# print("Part 1 real: ", part1(real_data, 71, 1024))
# print("Part 2 test: ", part2(test_data, 7))
# print("Part 2 real: ", part2(real_data, 71))
# wrong 165808