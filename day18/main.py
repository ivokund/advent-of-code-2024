from collections import namedtuple

test_data = """5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0"""


real_data = open("input.txt").read()
Point = namedtuple("Point", ["x", "y"])


def draw(obstacles, grid_size, highlight_nodes):
    grid = [["." for _ in range(grid_size)] for _ in range(grid_size)]
    for i, coord in enumerate(obstacles):
        grid[coord.y][coord.x] = '#'
    for i, coord in enumerate(highlight_nodes):
        grid[coord.y][coord.x] = 'o'
    for row in grid:
        print("".join(row))


def find_shortest_path_djikstra(start, end, obstacles, grid_size):
    visited = set()
    unvisited = set()
    came_from = {}
    for i in range(grid_size):
        for j in range(grid_size):
            unvisited.add(Point(i, j))
    distances = {point: float('inf') for point in unvisited}
    distances[start] = 0
    while unvisited:
        current = min(unvisited, key=lambda point: distances[point])
        unvisited.remove(current)
        visited.add(current)
        for direction in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_x = current.x + direction[0]
            new_y = current.y + direction[1]
            new_point = Point(new_x, new_y)
            if new_point in visited or new_point in obstacles or new_x < 0 or new_y < 0 or new_x >= grid_size or new_y >= grid_size:
                continue
            new_distance = distances[current] + 1
            if new_distance < distances[new_point]:
                came_from[new_point] = current
                distances[new_point] = new_distance

    if end not in came_from:
        return None, None
    path = []
    current = end
    while current != start:
        path.append(current)
        current = came_from[current]
    return distances[end], path


def parse(text, until):
    return [Point(*(int(num) for num in line.split(","))) for line in text.split('\n')[:until]]


def part1(text, grid_size, byte_count):
    coords = parse(text, byte_count)
    count, _ = find_shortest_path_djikstra(
        Point(0, 0),
        Point(grid_size-1, grid_size-1),
        coords,
        grid_size
    )
    return count


def part2(text, grid_size):
    all_byte_coords = parse(text, 5000)
    shortest_path = None
    start, end = Point(0, 0), Point(grid_size-1, grid_size-1)
    for idx, coord in enumerate(all_byte_coords):
        obstacles = all_byte_coords[:idx+1]
        if shortest_path is None or coord in shortest_path:
            _, shortest_path = find_shortest_path_djikstra(start, end, obstacles, grid_size)
        if shortest_path is None:
            return f"{coord.x},{coord.y}"


print("Part 1 test: ", part1(test_data, 7, 12))
print("Part 1 real: ", part1(real_data, 71, 1024))
print("Part 2 test: ", part2(test_data, 7))
print("Part 2 real: ", part2(real_data, 71))
