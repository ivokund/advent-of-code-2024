from collections import namedtuple
from heapq import heappush, heappop

test_data = """#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################"""

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


def parse(text):
    lines = [[1 if char == "#" else 0 for char in line] for line in text.split("\n")]
    return lines


def part1(text):
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
        came_from = {}

        while queue:
            current_cost, current_state = heappop(queue)
            if current_state in ends:
                return current_cost, came_from

            for next_state, move_cost in get_neighbors(current_state):
                new_cost = current_cost + move_cost

                if next_state not in costs or new_cost < costs[next_state]:
                    costs[next_state] = new_cost
                    heappush(queue, (new_cost, next_state))
                    came_from[next_state] = current_state
        return float('inf'), {}

    cost, path = find_path()
    return cost


print("Part 1 test: ", part1(test_data))
print("Part 1 real: ", part1(real_data))
