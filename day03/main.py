import re

test_data = """xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"""

real_data = open("input.txt").read()

def multiply(expression):
    parts = re.findall(r'\d{1,3}', expression)
    return int(parts[0]) * int(parts[1])

def part1(text):
    matches = re.findall(r'mul\(\d{1,3},\d{1,3}\)', text)
    return sum([multiply(match) for match in matches])


print("Part 1 test: ", part1(test_data))
print("Part 1 real: ", part1(real_data))
# print("Part 2 test: ", part2(test_data))
# print("Part 2 real: ", part2(real_data))
