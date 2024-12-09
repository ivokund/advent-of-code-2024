test_data = """1010101010101010101010"""

real_data = open("input.txt").read()


def parse(text):
    result = []


    print("10")
    print(str("10"))
    for id, char in enumerate(list(text)):
        print(id, id // 2)
        print("char", char)
        print("result before", result)
        add = (str(id // 2) if id % 2 == 0 else ".") * int(char)
        print("adding")
        print(add)
        result += add
        print(" ")
    return result


def part1(text):
    blocks = parse(text)
    print(blocks)
    for i in reversed(range(len(blocks))):
        if blocks[i] == ".":
            continue
        try:
            first_free_pos = blocks.index(".")
        except ValueError:
            break
        if first_free_pos > i:
            break
        blocks[first_free_pos], blocks[i] = blocks[i], blocks[first_free_pos]
        print(len(blocks))
        print("")
        print("")

    return sum([int(num) * idx for idx, num in enumerate(blocks) if num != "."])


print("Part 1 test: ", part1(test_data))
# print("Part 1 real: ", part1(real_data))
# print("Part 2 test: ", part2(test_data))
# print("Part 2 real: ", part2(real_data))

# wrong 90095094087
