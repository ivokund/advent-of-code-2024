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


def run_and_get_visited_nodes(map):
    visited_nodes = []
    while map.guard_in_map():
        map = map.move_step()
        visited_nodes.append(map.position_of_guard)
    return set(visited_nodes)


def part1(text):
    map = parse(text)
    return len(run_and_get_visited_nodes(map))


def part2(text):
    map = parse(text)

    original_path = run_and_get_visited_nodes(map)
    print("Original path", original_path)
    looping_positions = []
    i=0
    print(len(original_path))
    for coords in original_path:
        i+=1
        print("Checking", i, "of", len(original_path))
        # print("Obstacle at", coords)
        looping = False
        map_with_obstacle = Map(
            map.obstacles + [coords],
            map.position_of_guard,
            map.direction_of_guard,
            map.width,
            map.height
        )
        # print(map_with_obstacle)
        past_dirs_by_pos = {}
        while map_with_obstacle.guard_in_map() and not looping:
            # print("  - Guard at", map_with_obstacle.position_of_guard)
            new_map_with_obstacle = map_with_obstacle.move_step()
            if new_map_with_obstacle.position_of_guard in past_dirs_by_pos:
                # print("  - History", past_dirs_by_pos[new_map_with_obstacle.position_of_guard])
                direction_changed = new_map_with_obstacle.direction_of_guard not in past_dirs_by_pos[new_map_with_obstacle.position_of_guard]
                # print("  - Direction changed from ", past_dirs_by_pos[new_map_with_obstacle.position_of_guard], "to", new_map_with_obstacle.direction_of_guard, direction_changed)
                looping = not direction_changed
                # print("  - Looping", looping)
                if looping:
                    looping_positions += [coords]
            map_with_obstacle = new_map_with_obstacle
            if new_map_with_obstacle.position_of_guard not in past_dirs_by_pos:
                past_dirs_by_pos[new_map_with_obstacle.position_of_guard] = []
            past_dirs_by_pos[new_map_with_obstacle.position_of_guard] += [new_map_with_obstacle.direction_of_guard]

        # print("  - Looping", looping)
    print("Looping count", looping_positions)
    print("Looping count", len(set(looping_positions)))

# print("Part 1 test: ", part1(test_data))
# print("Part 1 real: ", part1(real_data))
# print("Part 2 test: ", part2(test_data))
print("Part 2 real: ", part2(real_data))
#  wrong: 1664