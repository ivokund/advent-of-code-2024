from collections import namedtuple
from heapq import heappush, heappop

test_data = """#####
#..E#
#S..#
#####"""

real_data = open("input.txt").read()

directions = {
    0: "^",
    1: ">",
    2: "v",
    3: "<",
}


def draw(grid, point):
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if (x, y) == (point[0], point[1]):
                print(directions[point.dir], end="")
            else:
                print("#" if cell == 1 else ".", end="")
        print()
    print()


def parse(text):
    lines = [[1 if char == "#" else 0 for char in line] for line in text.split("\n")]
    return lines

Point = namedtuple("Point", ["x", "y", "dir"])

def part1(text):
    grid = parse(text)
    start = Point(1, len(grid) - 2, 1)
    end = (len(grid[0]) - 2, 1)

    width = len(grid[0])
    height = len(grid)

    def get_neighbors(point):
        neighbors = []

        # First try moving forward
        moves = [(0,-1), (1,0), (0,1), (-1,0)]  # UP, RIGHT, DOWN, LEFT
        dx, dy = moves[point.dir]
        new_x, new_y = point.x + dx, point.y + dy

        if 0 <= new_x < width and 0 <= new_y < height and grid[new_y][new_x] == 0:
            neighbors.append((Point(new_x, new_y, point.dir), 1))
            return neighbors


        # Only if we can't move forward, add rotations
        clockwise = (point.dir + 1) % 4
        counterclockwise = (point.dir - 1) % 4
        neighbors.append((Point(point.x, point.y, clockwise), 1002))
        neighbors.append((Point(point.x, point.y, counterclockwise), 1002))

        return neighbors

    def find_path(start, end):
        queue = [(0, start)]
        costs = {start: 0}
        came_from = {}

        print(f"\nStarting at {start}, trying to reach {end}")

        while queue:
            print("\nCurrent queue:", [(cost, f"({s.x},{s.y},{directions[s.dir]})") for cost,s in queue])
            print("Current costs:", {f"({s.x},{s.y},{directions[s.dir]})": c for s,c in costs.items()})

            current_cost, current_state = heappop(queue)
            current_pos = (current_state.x, current_state.y)

            print(f"\nExploring: ({current_state.x},{current_state.y},{directions[current_state.dir]}) with cost {current_cost}")

            if current_pos == end:
                return current_cost, came_from

            for next_state, move_cost in get_neighbors(current_state):
                new_cost = current_cost + move_cost

                print(f"  Considering: ({next_state.x},{next_state.y},{directions[next_state.dir]}) with new cost {new_cost}")

                if next_state not in costs or new_cost < costs[next_state]:
                    print(f"    -> Queueing this path (better than previous cost)")
                    costs[next_state] = new_cost
                    heappush(queue, (new_cost, next_state))
                else:
                    print(f"    Already known cost: {costs[next_state]}")
                    print(f"    -> Skipping (not better than previous)")

            came_from[current_state] = came_from.get(current_state, current_state)

        return float('inf'), {}

    draw(grid, start)

    cost, path = find_path(start, end)
    print(cost, path)
    for point in path.values():
        draw(grid, point)
    return len(path)

print("Part 1 test: ", part1(test_data))
