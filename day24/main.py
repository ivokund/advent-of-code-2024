import re
import unittest
from itertools import combinations

test_data = """x00: 1
x01: 1
x02: 1
y00: 0
y01: 1
y02: 0

x00 AND y00 -> z00
x01 XOR y01 -> z01
x02 OR y02 -> z02"""

test_data_2 = """x00: 0
x01: 1
x02: 0
x03: 1
x04: 0
x05: 1
y00: 0
y01: 0
y02: 1
y03: 1
y04: 0
y05: 1

x00 AND y00 -> z05
x01 AND y01 -> z02
x02 AND y02 -> z01
x03 AND y03 -> z03
x04 AND y04 -> z04
x05 AND y05 -> z00"""


real_data = open("input.txt").read()


def parse(text):
    p1, p2 = text.strip().split("\n\n")
    signals = {name: (True if value == "1" else False) for name, value in [line.split(": ") for line in p1.split("\n")]}

    gates = {}
    for line in p2.split("\n"):
        parts = re.search(r"(.+) (.+) (.+) -> (.+)", line).groups()
        gates[parts[3]] = (parts[1], parts[0], parts[2])
    return signals, gates


def get_value(op, a, b):
    if op == 'AND':
        return a and b
    elif op == 'OR':
        return a or b
    elif op == 'XOR':
        return a ^ b


def get_z_value(signals, gates):
    resolved = signals.copy()
    queue = list(gates.keys())
    while queue:
        name = queue.pop(0)
        op, a, b = gates[name]
        if a in resolved and b in resolved:
            resolved[name] = get_value(op, resolved[a], resolved[b])
        else:
            queue.append(name)

    sorted_z = sorted([key for key in resolved.keys() if key.startswith("z")], reverse=True)
    int_values = "".join([str(int(resolved[key])) for key in sorted_z])

    return int(int_values, 2)

def generate_source_bits(x, y):
    x_binary = f'{x:b}'
    y_binary = f'{y:b}'
    signals = {}
    for i, bit in enumerate(x_binary):
        signals[f'x{i:02d}'] = True if bit == '1' else False
    for i, bit in enumerate(y_binary):
        signals[f'y{i:02d}'] = True if bit == '1' else False
    return signals


def part1(text):
    signals, gates = parse(text)
    return get_z_value(signals, gates)


def get_sorted_csv(swaps):
    return ",".join(sorted(list(swaps.keys()) + list(swaps.values())))


def part2(text):
    _, gates = parse(text)
    signals = generate_source_bits(13, 11)

    # todo
    return get_sorted_csv(last_swaps)


class Day24Tests(unittest.TestCase):
    def test_parse(self):
        wires, gates = parse(test_data)
        self.assertEqual(wires["x00"], True)
        self.assertEqual(wires["y00"], False)
        self.assertEqual(gates["z00"], ('AND', 'x00', 'y00'))

    def test_part1(self):
        self.assertEqual(part1(test_data), 4)
        self.assertEqual(part1(real_data), 55920211035878)

    def test_generate_source(self):
        self.assertEqual(generate_source_bits(13, 11), {
            'x00': True, 'x01': True, 'x02': False, 'x03': True,
            'y00': True, 'y01': False, 'y02': True, 'y03': True
        })

    def test_format_answer(self):
        input = {
            'z05': 'z00',
            'z02': 'z01',
        }
        self.assertEqual(get_sorted_csv(input), 'z00,z01,z02,z05')

