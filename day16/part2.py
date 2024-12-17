from collections import namedtuple
from heapq import heappush, heappop

# 4 turns, forward 7
#
test_data = """#######
#....E#
##.#.##
#.....#
#S#...#
#######"""

test_data = """###############
#.......#....O#
#.#.###.#.###O#
#.....#.#...#O#
#.###.#####.#O#
#.#.#.......#O#
#.#.#####.###O#
#..OOOOOOOOO#O#
###O#O#####O#O#
#OOO#O....#O#O#
#O#O#O###.#O#O#
#OOOOO#...#O#O#
#O###.#.#.#O#O#
#O..#.....#OOO#
###############"""

real_data = open("input.txt").read()

directions = {
    0: "^",
    1: ">",
    2: "v",
    3: "<",
}

Point = namedtuple("Point", ["x", "y", "dir"])

def print_point(self):
    return f"({self.x},{self.y},{directions[self.dir]})"
Point.__str__ = print_point

def draw(grid, point):
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if (x, y) == (point[0], point[1]):
                print(directions[point.dir], end="")
            else:
                print("#" if cell == 1 else ".", end="")
        print()
    print()

def draw_all(grid, points):
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if any((x, y) == (point.x, point.y) for point in points):
                print("O", end="")
            else:
                print("#" if cell == 1 else ".", end="")
        print()
    print()


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

        # First try moving forward
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

        print(f"\nStarting at {start}, trying to reach {ends}")
        while queue:
            print("\nCurrent queue:", [(cost, f"({s.x},{s.y},{directions[s.dir]})") for cost,s in queue])
            print("Current costs:", {f"({s.x},{s.y},{directions[s.dir]})": c for s,c in costs.items()})

            current_cost, current_state = heappop(queue)
            current_pos = (current_state.x, current_state.y)
            print(f"\nExploring: ({current_state.x},{current_state.y},{directions[current_state.dir]}) with cost {current_cost}")

            # print("  current state:", current_state)
            if current_state in ends and current_cost <= min_cost:
                min_cost = min(min_cost, current_cost)
                continue

            for next_state, move_cost in get_neighbors(current_state):
                new_cost = current_cost + move_cost
                print(f"  Considering: ({next_state.x},{next_state.y},{directions[next_state.dir]}) with new cost {new_cost}")

                if new_cost < min_cost:
                    if next_state not in costs or new_cost < costs[next_state]:
                        print(f"    -> Queueing {next_state} path (cost {new_cost} is better than previous: {costs[next_state] if next_state in costs else 'None'})")
                        costs[next_state] = new_cost
                        heappush(queue, (new_cost, next_state))
                        came_from[next_state] = [current_state]
                    elif new_cost == costs[next_state]:
                        print(f"    -> Adding {next_state} to came_from[{current_state}] (equal cost)")
                        came_from[next_state].append(current_state)
                else:
                    print(f"    Skipping {next_state} (cost {new_cost} is not better than min_cost {min_cost})")


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

    # draw(grid, start)

    cost, came_from = find_path()
    print(f"Shortest path cost: {cost}")

    all_paths = []
    for end_state in ends:
        if end_state in came_from:
            find_all_paths(came_from, start, end_state, [], all_paths)

    print(f"Number of best paths found: {len(all_paths)}")

    unique_points_in_all_paths = set()
    for path in all_paths:
        for point in path:
            unique_points_in_all_paths.add(point)

    draw_all(grid, unique_points_in_all_paths)

    return len(unique_points_in_all_paths)

    # for i, path in enumerate(all_paths, start=1):
    #     print(f"\nPath {i}:")
    #     for point in path:
    #         draw(grid, point)


print("Part 2 test: ", part2(test_data))
# print("Part 1 real: ", part2(real_data))
