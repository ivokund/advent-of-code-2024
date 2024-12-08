test_data = """............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............"""

real_data = open("input.txt").read()


def parse(text):
    lines = text.split("\n")
    coords = {}
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char != ".":
                if char not in coords:
                    coords[char] = []
                coords[char].append((x, y))
    return coords, len(lines[0]), len(lines)


def run(text, use_resonance=False):
    coords, width, height = parse(text)

    def is_in_map(coords):
        x, y = coords
        return 0 <= x < width and 0 <= y < height

    all_vectors = []  # start pos, vector
    antinodes = []
    for key in coords:
        for coord1 in coords[key]:
            for coord2 in coords[key]:
                if coord1 != coord2:
                    dx, dy = (coord2[0] - coord1[0]), (coord2[1] - coord1[1])
                    all_vectors.append([coord1, (dx, dy)])
                    antinode = (coord1[0] - dx), (coord1[1] - dy)
                    if antinode not in antinodes and is_in_map(antinode):
                        antinodes.append(antinode)
                    if use_resonance:
                        while is_in_map(antinode):
                            antinode = (antinode[0] + dx), (antinode[1] + dy)
                            if antinode not in antinodes and is_in_map(antinode):
                                antinodes.append(antinode)
    part1_answer = len(antinodes)
    if not use_resonance:
        return part1_answer

    resonated_nodes = set([])
    for start_pos, vector in all_vectors:
        current_pos = start_pos
        while is_in_map(current_pos):
            resonated_nodes.add(current_pos)
            current_pos = (current_pos[0] + vector[0]), (current_pos[1] + vector[1])
        current_pos = start_pos
        while is_in_map(current_pos):
            resonated_nodes.add(current_pos)
            current_pos = (current_pos[0] - vector[0]), (current_pos[1] - vector[1])

    part2_answer = len(resonated_nodes)
    return part2_answer


print("Part 1 test: ", run(test_data))
print("Part 1 real: ", run(real_data))
print("Part 2 test: ", run(test_data, True))
print("Part 2 real: ", run(real_data, True))
