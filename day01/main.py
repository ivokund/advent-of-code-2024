from collections import Counter

testData = """3   4
4   3
2   5
1   3
3   9
3   3
"""

realData = open("input.txt").read()

def parse(input):
    data = [[int(item) for item in line.split()] for line in input.split("\n") if line]
    col1 = [item[0] for item in data]
    col2 = [item[1] for item in data]
    return sorted(col1), sorted(col2)

def part1(input):
    sum = 0
    col1, col2 = parse(input)
    for i in range(len(col1)):
        sum += abs(col2[i] - col1[i])
    return sum

def part2(input):
    col1, col2 = parse(input)
    counter = Counter(col2)
    sum = 0
    for value in col1:
        sum += value * counter[value]
    return sum

print("Part 1 test: ", part1(testData))
print("Part 1 real: ", part1(realData))
print("Part 2 test: ", part2(testData))
print("Part 2 real: ", part2(realData))
