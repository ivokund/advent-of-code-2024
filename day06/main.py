test_data = """....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#..."""
real_data = open("input.txt").read()


def parse(text):
    lines = text.split("\n")
    position_of_guard = None
    obstacles = []
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char == "^":
                position_of_guard = (x, y)
            elif char != ".":
                obstacles += [(x, y)]

    direction_of_guard = 0, -1  # up
    return Map(obstacles, position_of_guard, direction_of_guard, len(lines[0]), len(lines))


class Map:
    def __init__(self, obstacles, position_of_guard, direction_of_guard, width, height, past_positions=[]):
        self.obstacles = obstacles
        self.position_of_guard = position_of_guard
        self.direction_of_guard = direction_of_guard
        self.width = width
        self.height = height
        # print(self)

    def move_step(self):
        x, y = self.position_of_guard
        dx, dy = self.direction_of_guard
        new_position = (x + dx, y + dy)
        if new_position in self.obstacles:
            new_x, new_y = -dy, dx  # rotate 90 degrees right
            return Map(self.obstacles, self.position_of_guard, (new_x, new_y), self.width, self.height)
        else:
            return Map(self.obstacles, new_position, self.direction_of_guard, self.width, self.height)

    def guard_in_map(self):
        x, y = self.position_of_guard
        return 0 <= x < self.width and 0 <= y < self.height

    def __str__(self):
        result = ""
        guard_by_char = {
            (0, -1): "^",
            (0, 1): "v",
            (-1, 0): "<",
            (1, 0): ">"
        }
        for y in range(self.height):
            for x in range(self.width):
                if (x, y) in self.obstacles:
                    result += "#"
                elif (x, y) == self.position_of_guard:
                    result += guard_by_char[self.direction_of_guard]
                else:
                    result += "."
            result += "\n"
        return result


def part1(text):
    map = parse(text)

    visited_nodes = [map.position_of_guard]
    while map.guard_in_map():
        map = map.move_step()
        visited_nodes.append(map.position_of_guard)

    return len(set(visited_nodes)) - 1


print("Part 1 test: ", part1(test_data))
print("Part 1 real: ", part1(real_data))
# print("Part 2 test: ", part2(test_data))
# print("Part 2 real: ", part2(real_data))
#