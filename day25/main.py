import unittest

test_data = """#####
.####
.####
.####
.#.#.
.#...
.....

#####
##.##
.#.##
...##
...#.
...#.
.....

.....
#....
#....
#...#
#.#.#
#.###
#####

.....
.....
#.#..
###..
###.#
###.#
#####

.....
.....
.....
#....
#.#..
#.#.#
#####"""


real_data = open("input.txt").read()


def parse(text):
    blocks = text.split("\n\n")
    locks, keys = [], []

    def as_col(block):
        return ["".join([line[i] for line in block]) for i in range(len(block[0]))]

    for block in blocks:
        lines = block.split("\n")
        if lines[0] == '#####': # lock
            lines = lines[1:]
            as_cols = as_col(lines)
            counts = [len(c.rstrip('.')) for c in as_cols]
            locks.append(counts)
        elif lines[6] == '#####':
            lines = lines[:6]
            as_cols = as_col(lines)
            counts = [len(c.lstrip('.')) for c in as_cols]
            keys.append(counts)
        else:
            print(lines)
            raise ValueError("Invalid block")

    return locks, keys


def fits(key, lock):
    for i in range(len(key)):
        if key[i] + lock[i] > 5:
            return False
    return True


def part1(text):
    locks, keys = parse(text)

    unique_fits = 0
    for lock in locks:
        for key in keys:
            if fits(key, lock):
                unique_fits += 1

    return unique_fits


class Day25Tests(unittest.TestCase):
    def test_parse(self):
        locks, keys = parse(test_data)
        self.assertEqual(locks, [
            [0,5,3,4,3],
            [1,2,0,5,3]
        ])
        self.assertEqual(keys, [
            [5,0,2,1,3],
            [4,3,4,0,2],
            [3,0,2,0,1]
        ])

    def test_fit(self):
        self.assertEqual(fits([0,5,3,4,3], [5,0,2,1,3]), False)
        self.assertEqual(fits([0,5,3,4,3], [3,0,2,0,1]), True)

    def test_part1(self):
        self.assertEqual(part1(test_data), 3)
        self.assertEqual(part1(real_data), 3127)
