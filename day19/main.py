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


def solve(text):
    patterns, designs = parse(text)

    def get_suitable_patterns(remaining_text: Text):
        return [pattern for pattern in patterns
                if remaining_text.startswith(pattern)
                and len(pattern) <= len(remaining_text)]

    combo_counts_by_pattern = {}

    def get_pattern_combos(design):
        def find_pattern_combos(remaining_pattern, prev_combos: int):
            if remaining_pattern in combo_counts_by_pattern:
                return combo_counts_by_pattern[remaining_pattern] * prev_combos

            if len(remaining_pattern) == 0:
                return True

            patterns = get_suitable_patterns(remaining_pattern)
            num_of_combos = 0
            for next_pattern in patterns:
                remainder = remaining_pattern[len(next_pattern):]
                num_of_combos += find_pattern_combos(remainder, prev_combos)
            combo_counts_by_pattern[remaining_pattern] = num_of_combos
            return num_of_combos * prev_combos

        return find_pattern_combos(design, 1)

    possibles = [get_pattern_combos(design) for design in designs]

    part1 = len([design for design in possibles if design])
    part2 = sum(possibles)
    return part1, part2


part1_test, part2_test = solve(test_data)
part1_real, part2_real = solve(real_data)

print("Part 1 test: ", part1_test)
print("Part 1 real: ", part1_real)
print("Part 2 test: ", part2_test)
print("Part 2 real: ", part2_real)

