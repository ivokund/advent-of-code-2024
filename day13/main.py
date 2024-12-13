import re
from collections import namedtuple

test_data = """Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279"""

real_data = open("input.txt").read()

Movement = namedtuple("Movement", ["dx", "dy"])
Point = namedtuple("Point", ["x", "y"])
Machine = namedtuple("Machine", ["a", "b", "target"])


def part1(text):
    blocks = [block.split("\n") for block in text.split("\n\n")]
    machines = [[[int(num) for num in re.findall(r'\d+', line.split(": ")[1])] for line in block] for block in blocks]
    machines = [Machine(Movement(*machine[0]), Movement(*machine[1]), Point(*machine[2])) for machine in machines]

    # loop 100 times
    def run_machine(machine):
        for a_movements in range(100):
            for b_movements in range(100):
                pos = Point(machine.a.dx * a_movements + machine.b.dx * b_movements, machine.a.dy * a_movements + machine.b.dy * b_movements)
                if pos == machine.target:
                    # print("Found target at A={}, B={}".format(a_movements, b_movements))
                    return a_movements * 3 + 1 * b_movements

    return sum([run_machine(machine) or 0 for machine in machines])

print("Part 1 test: ", part1(test_data))
print("Part 1 real: ", part1(real_data))
# print("Part 2 test: ", part2(test_data))
# print("Part 2 real: ", part2(real_data))