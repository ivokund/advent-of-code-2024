test_data = """190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20"""
real_data = open("input.txt").read()


def parse(text):
    equations = [line.split(": ") for line in text.split("\n")]
    return [[int(equation[0])] + [int(operand) for operand in equation[1].split()] for equation in equations]


def part1(text):
    equations = parse(text)

    def is_true(expected_result, operand1, operand2, remaining_operands):
        if (operand1 * operand2 == expected_result or operand1 + operand2 == expected_result) and len(remaining_operands) == 0:
            return True
        if len(remaining_operands) > 0:
            if is_true(expected_result, operand1 * operand2, remaining_operands[0], remaining_operands[1:]):
                return True
            elif is_true(expected_result, operand1 + operand2, remaining_operands[0], remaining_operands[1:]):
                return True
        return False

    true_equations = [equation for equation in equations if is_true(equation[0], equation[1], equation[2], equation[3:])]

    return sum([equation[0] for equation in true_equations])


print("Part 1 test: ", part1(test_data))
print("Part 1 real: ", part1(real_data))
# print("Part 2 test: ", part2(test_data))
# print("Part 2 real: ", part2(real_data))
