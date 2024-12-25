import re
import unittest
from collections import namedtuple

test_data = """x00: 1
x01: 1
x02: 1
y00: 0
y01: 1
y02: 0

x00 AND y00 -> z00
x01 XOR y01 -> z01
x02 OR y02 -> z02"""


real_data = open("input.txt").read()


def parse(text):
    p1, p2 = text.strip().split("\n\n")
    wires = {name: (True if value == "1" else False) for name, value in [line.split(": ") for line in p1.split("\n")]}

    for line in p2.split("\n"):
        parts = re.search(r"(.+) (.+) (.+) -> (.+)", line).groups()
        wires[parts[3]] = (parts[1], parts[0], parts[2])
    return wires

def get_value(op, a, b):
    if op == 'AND':
        return a and b
    elif op == 'OR':
        return a or b
    elif op == 'XOR':
        return a ^ b
def resolve_all(wires):
    resolved = {}
    queue = list(wires.keys())
    while queue:
        name = queue.pop(0)
        if isinstance(wires[name], bool):
            resolved[name] = wires[name]
        else:
            op, a, b = wires[name]
            if a in resolved and b in resolved:
                resolved[name] = get_value(op, resolved[a], resolved[b])
            else:
                queue.append(name)
    return resolved

def part1(text):
    wires = parse(text)

    result = resolve_all(wires)

    sorted_wires_with_z = sorted([key for key in result.keys() if key.startswith("z")], reverse=True)
    int_values = "".join([str(int(result[key])) for key in sorted_wires_with_z])

    return int(int_values, 2)


class Day24Tests(unittest.TestCase):
    def test_parse(self):
        parsed = parse(test_data)
        self.assertEqual(parsed["x00"], True)
        self.assertEqual(parsed["y00"], False)
        self.assertEqual(parsed["z00"], ('AND', 'x00', 'y00'))

    def test_part1(self):
        self.assertEqual(part1(test_data), 4)
        self.assertEqual(part1(real_data), 55920211035878)




