test_data = """7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
"""

real_data = open("input.txt").read()


def parse(text_input):
    return [[int(num) for num in line.split()] for line in text_input.split("\n") if line]


def is_safe(report):
    deltas = [report[i] - report[i+1] for i in range(len(report) - 1)]
    abs_deltas = [abs(delta) for delta in deltas]

    return (min(abs_deltas) >= 0
            and max(abs_deltas) <= 3
            and (all(delta > 0 for delta in deltas) or (all(delta < 0 for delta in deltas))))


def part1(text):
    reports = parse(text)
    safe_count = filter(is_safe, reports)
    return len(list(safe_count))


def part2(text):
    reports = parse(text)

    def is_safe_with_removing_one(report):
        for i in range(len(report)):
            new_report = report[:i] + report[i+1:]
            if is_safe(new_report):
                return True
        return False

    safe_count = filter(is_safe_with_removing_one, reports)
    return len(list(safe_count))


print("Part 1 test: ", part1(test_data))
print("Part 1 real: ", part1(real_data))
print("Part 2 test: ", part2(test_data))
print("Part 2 real: ", part2(real_data))
