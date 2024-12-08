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

    # return Map(coords, len(lines[0]), len(lines))


class Map:
    def __init__(self, coords, width, height):
        self.coords = coords
        self.width = width
        self.height = height


    def coord_in_map(self, coords):
        x, y = coords
        return 0 <= x < self.width and 0 <= y < self.height

    # def __str__(self):
    #     result = ""
    #
    #     for y in range(self.height):
    #         for x in range(self.width):
    #             if (x, y) in self.obstacles:
    #                 result += "#"
    #             else:
    #                 result += "."
    #         result += "\n"
    #     return result


def run(text, use_resonance=False):
    coords, width, height = parse(text)

    def is_in_map(coords):
        x, y = coords
        return 0 <= x < width and 0 <= y < height

    antinodes = []
    for key in coords:
        # print("For ", key)
        for coord1 in coords[key]:
            for coord2 in coords[key]:
                if coord1 != coord2:
                    # print("Points: ", coord1, coord2)
                    dx, dy = (coord2[0] - coord1[0]), (coord2[1] - coord1[1])
                    antinode = (coord1[0] + 2 * dx), (coord1[1] + 2 * dy)
                    if antinode not in antinodes and is_in_map(antinode):
                        antinodes.append(antinode)
                    # print("Antinode 1: ", antinode)

    # print(coords)
    # print(antinodes)
    return len(antinodes)

print("Part 1 test: ", run(test_data))
print("Part 1 real: ", run(real_data))
# print("Part 2 test: ", part2(test_data))
# print("Part 2 real: ", part2(real_data))
#  wrong: 1664