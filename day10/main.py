test_data = """89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732"""

real_data = open("input.txt").read()


def solve(text):
    grid = [[int(num) for num in list(row)] for row in text.split("\n")]

    width = len(grid[0])
    height = len(grid)

    def find_next_valid_positions(pos):
        deltas = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        val = grid[pos[1]][pos[0]]
        positions = set([])
        for dx, dy in deltas:
            new_x = pos[0] + dx
            new_y = pos[1] + dy
            if 0 <= new_x < width and 0 <= new_y < height and grid[new_y][new_x] == val + 1:
                positions.add((new_x, new_y))
        return positions


    def find_paths_from(start):
        ends = set([])
        paths = []

        def find_path(pos, path):
            if grid[pos[1]][pos[0]] == 9:
                ends.add(pos)
                paths.append(path)
                return

            next_positions = find_next_valid_positions(pos)
            if not next_positions:
                return
            for next_pos in next_positions:
                find_path(next_pos, path + [next_pos])

        find_path(start, [start])
        return ends, paths

    start_positions = []
    for y, row in enumerate(grid):
        for x, num in enumerate(row):
            if num == 0:
                start_positions.append((x, y))

    ends = []
    paths = []
    for start in start_positions:
        end, path = find_paths_from(start)
        ends += end
        paths += path

    return len(ends), len(paths)


test = solve(test_data)
real = solve(real_data)

print("Part 1 test: ", test[0])
print("Part 1 real: ", real[0])
print("Part 2 test: ", test[1])
print("Part 2 real: ", real[1])
