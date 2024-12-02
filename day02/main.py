from collections import Counter

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

def get_bad_level_count(report):
    print("REPORT: ", report)
    number_of_bad_levels = 0
    sign = report[0] > report[1]
    print("decreasing: ", sign)
    for i in range(len(report) - 1):
        delta = abs(report[i] - report[i+1])
        print("i: ", i, "delta: ", delta)
        bad_delta = delta > 3 or delta < 1
        # check if the sign is the same
        bad_sign = (report[i] > report[i+1]) is not sign
        print("bad_delta", bad_delta)
        print("bad_sign", bad_sign)
        if bad_delta or bad_sign:
            number_of_bad_levels += 1
    print("SAFE" if number_of_bad_levels == 0 else "UNSAFE")
    print("bad levels: ", number_of_bad_levels)
    print("")
    return number_of_bad_levels

def part1(text):
    reports = parse(text)
    # print(get_bad_level_count(reports[0]))
    safe_count = filter(lambda x: get_bad_level_count(x) == 0, reports)
    return len(list(safe_count))

def part2(text):
    reports = parse(text)
    # print(get_bad_level_count(reports[0]))
    safe_count = filter(lambda x:
                        get_bad_level_count(x) <= 1
                        , reports)
    return len(list(safe_count))


print("Part 1 test: ", part1(test_data))
print("Part 1 real: ", part1(real_data))
# print("Part 2 test: ", part2(test_data))
# print("Part 2 real: ", part2(real_data))
