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
    directions_by_pos = {}
    while map.guard_in_map():
        map = map.move_step()
        visited_nodes.append(map.position_of_guard)
        directions_by_pos[map.position_of_guard] = map.direction_of_guard
    return set(visited_nodes), directions_by_pos


def part1(text):
    map = parse(text)
    nodes, _ = run_and_get_visited_nodes(map)
    return len(nodes)


def part2(text):
    map = parse(text)

    original_path, directions = run_and_get_visited_nodes(map)

    potential_obstructions = set([])
    for node in original_path:
        direction = directions[node]
        if direction == (0, -1): # up
            for y in range(0, node[1]):
                potential_obstructions.add((node[0], y))
        elif direction == (0, 1): # down
            for y in range(node[1], map.height):
                potential_obstructions.add((node[0], y))
        elif direction == (-1, 0): # left
            for x in range(0, node[0]):
                potential_obstructions.add((x, node[1]))
        elif direction == (1, 0): # right
            for x in range(node[0], map.width):
                potential_obstructions.add((x, node[1]))

    looping_positions = []
    print(len(potential_obstructions))
    for coords in potential_obstructions:
        looping = False
        map_with_obstacle = Map(
            map.obstacles + [coords],
            map.position_of_guard,
            map.direction_of_guard,
            map.width,
            map.height
        )
        past_dirs_by_pos = {}
        while map_with_obstacle.guard_in_map() and not looping:
            new_map_with_obstacle = map_with_obstacle.move_step()
            if new_map_with_obstacle.position_of_guard in past_dirs_by_pos:
                direction_changed = new_map_with_obstacle.direction_of_guard not in past_dirs_by_pos[new_map_with_obstacle.position_of_guard]
                looping = not direction_changed
                if looping:
                    looping_positions += [coords]
            map_with_obstacle = new_map_with_obstacle
            if new_map_with_obstacle.position_of_guard not in past_dirs_by_pos:
                past_dirs_by_pos[new_map_with_obstacle.position_of_guard] = []
            past_dirs_by_pos[new_map_with_obstacle.position_of_guard] += [new_map_with_obstacle.direction_of_guard]

    return len(set(looping_positions))


print("Part 1 test: ", part1(test_data))
print("Part 1 real: ", part1(real_data))
print("Part 2 test: ", part2(test_data))
print("Part 2 real: ", part2(real_data))
