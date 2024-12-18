from collections import namedtuple
from heapq import heappush, heappop

test_data = """#################
#...#...#...#..O#
#.#.#.#.#.#.#.#O#
#.#.#.#...#...#O#
#.#.#.#.###.#.#O#
#OOO#.#.#.....#O#
#O#O#.#.#.#####O#
#O#O..#.#.#OOOOO#
#O#O#####.#O###O#
#O#O#..OOOOO#OOO#
#O#O###O#####O###
#O#O#OOO#..OOO#.#
#O#O#O#####O###.#
#O#O#OOOOOOO..#.#
#O#O#O#########.#
#O#OOO..........#
#################"""

real_data = open("input.txt").read()

directions = {
    0: "^",
    1: ">",
    2: "v",
    3: "<",
}

Point = namedtuple("Point", ["x", "y", "dir"])


def parse(text):
    lines = [[1 if char == "#" else 0 for char in line] for line in text.split("\n")]
    return lines


def part2(text):
    grid = parse(text)
    start = Point(1, len(grid) - 2, 1)
    ends = set([Point(len(grid[0]) - 2, 1, direction) for direction in directions.keys()])

    width = len(grid[0])
    height = len(grid)

    def get_neighbors(point):
        neighbors = []

        moves = [(0,-1), (1,0), (0,1), (-1,0)]  # UP, RIGHT, DOWN, LEFT
        dx, dy = moves[point.dir]
        new_x, new_y = point.x + dx, point.y + dy

        if width > new_x >= 0 == grid[new_y][new_x] and 0 <= new_y < height:
            neighbors.append((Point(new_x, new_y, point.dir), 1))

        clockwise = (point.dir + 1) % 4
        counterclockwise = (point.dir - 1) % 4
        neighbors.append((Point(point.x, point.y, clockwise), 1000))
        neighbors.append((Point(point.x, point.y, counterclockwise), 1000))

        return neighbors

    def find_path():
        queue = [(0, start)]
        costs = {start: 0}
        came_from = {start: []}
        min_cost = float('inf')

        while queue:
            current_cost, current_state = heappop(queue)

            # print("  current state:", current_state)
            if current_state in ends and current_cost <= min_cost:
                min_cost = min(min_cost, current_cost)
                continue

            for next_state, move_cost in get_neighbors(current_state):
                new_cost = current_cost + move_cost

                if new_cost < min_cost:
                    if next_state not in costs or new_cost < costs[next_state]:
                        costs[next_state] = new_cost
                        heappush(queue, (new_cost, next_state))
                        came_from[next_state] = [current_state]
                    elif new_cost == costs[next_state]:
                        came_from[next_state].append(current_state)

        return min_cost, came_from

    def find_all_paths(came_from, start, end, path, all_paths):
        path.append(end)
        if end == start:
            all_paths.append(path[::-1])
        else:
            if end in came_from:
                for prev_state in came_from[end]:
                    find_all_paths(came_from, start, prev_state, path, all_paths)
        path.pop()

    cost, came_from = find_path()

    all_paths = []
    for end_state in ends:
        if end_state in came_from:
            find_all_paths(came_from, start, end_state, [], all_paths)

    unique_points_in_all_paths = set()
    for path in all_paths:
        for point in path:
            unique_points_in_all_paths.add(Point(point.x, point.y, 1))

    return len(unique_points_in_all_paths)

print("Part 2 test: ", part2(test_data))
print("Part 1 real: ", part2(real_data))
