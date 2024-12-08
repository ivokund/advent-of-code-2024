test_data = """T.........
...T......
.T........
..........
..........
..........
..........
..........
..........
.........."""

test_data2 = """............
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
        print("For ", key)
        for coord1 in coords[key]:
            for coord2 in coords[key]:
                if coord1 != coord2:
                    print("Points: ", coord1, coord2)
                    dx, dy = (coord2[0] - coord1[0]), (coord2[1] - coord1[1])
                    antinode = (coord1[0] - dx), (coord1[1] - dy)
                    if antinode not in antinodes and is_in_map(antinode):
                        antinodes.append(antinode)
                        # extra_coords.append(coord1)
                        # extra_coords.append(coord2)
                    if use_resonance:
                        while is_in_map(antinode):
                            antinode = (antinode[0] + dx), (antinode[1] + dy)
                            print("Antinode: ", antinode)

                            if antinode not in antinodes and is_in_map(antinode):
                                antinodes.append(antinode)
                                # extra_coords.append(coord1)
                                # extra_coords.append(coord2)

    print(antinodes)
    return len(antinodes)


print("Part 1 test: ", run(test_data2))
print("Part 1 real: ", run(real_data))
# print("Part 2 test: ", run(test_data2, True))
# print("Part 2 real: ", part2(real_data))
