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


def is_true(expected_result, operand1, operand2, remaining_operands, operations):
    if len(remaining_operands) == 0:
        return any([operation(operand1, operand2) == expected_result for operation in operations])
    else:
        return any([is_true(
                expected_result,
                operation(operand1, operand2),
                remaining_operands[0],
                remaining_operands[1:],
                operations
        ) for operation in operations])


def part1(text):
    equations = parse(text)
    operations = [
        lambda a, b: a + b,
        lambda a, b: a * b,
    ]

    return sum(
        [equation[0] for equation in equations if is_true(
            equation[0],
            equation[1],
            equation[2],
            equation[3:],
            operations
        )]
    )


def part2(text):
    equations = parse(text)
    operations = [
        lambda a, b: a + b,
        lambda a, b: a * b,
        lambda a, b: int(str(a) + str(b)),
    ]

    return sum(
        [equation[0] for equation in equations if is_true(
            equation[0],
            equation[1],
            equation[2],
            equation[3:],
            operations
        )]
    )


print("Part 1 test: ", part1(test_data))
print("Part 1 real: ", part1(real_data))
print("Part 2 test: ", part2(test_data))
print("Part 2 real: ", part2(real_data))
