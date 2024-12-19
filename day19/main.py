from typing import Text

test_data = """r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb"""

real_data = open("input.txt").read()


def parse(text):
    patterns, designs_text = text.split("\n\n")
    return patterns.split(", "), designs_text.split("\n")


def part1(text):
    patterns, designs = parse(text)
    # patterns = sorted(patterns, key=len, reverse=True)

    def get_suitable_patterns(remaining_text: Text):
        return [pattern for pattern in patterns
                if remaining_text.startswith(pattern)
                and len(pattern) <= len(remaining_text)]

    # print(f'Total designs: {len(designs)}')
    i = 0

    is_possible_by_pattern = {}
    def is_possible(design):
        nonlocal i
        # print(f'Checking design {i}.: {design}..')
        i += 1

        def find_pattern_combos(remaining_pattern, nesting = 0):
            if remaining_pattern in is_possible_by_pattern:
                return is_possible_by_pattern[remaining_pattern]

            if len(remaining_pattern) == 0:
                # print(f'{"." * nesting}END!')
                return True

            patterns = get_suitable_patterns(remaining_pattern)
            # print(f'{"." * nesting}  suitable patterns: {patterns}')
            for pattern in patterns:
                # print(f'{"." * nesting}    using pattern: {pattern}')
                remainder = remaining_pattern[len(pattern):]

                # print(f'{"." * nesting}    remainder: {remainder}')
                if find_pattern_combos(remainder, nesting + 2):
                    is_possible_by_pattern[remainder] = True
                    return True
                else:
                    is_possible_by_pattern[remainder] = False
        f = find_pattern_combos(design, 0)
        # print(f'Found: {f}')
        return f

    # designs = [designs[3]]

    # used = is_possible(designs[2])
    # print(used)


    possibles = [design for design in designs if is_possible(design)]
    # print(possibles)
    return len(possibles)



print("Part 1 test: ", part1(test_data))
print("Part 1 real: ", part1(real_data))
# print("Part 2 test: ", part2(test_data))
# print("Part 2 real: ", part2(real_data))
