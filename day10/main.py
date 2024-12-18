from collections import namedtuple

test_data = """89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732"""

real_data = open("input.txt").read()
# Point = namedtuple("Point", ["x", "y"])




def part1(text):
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
        def find_path(pos, path):
            # print("Finding paths from ", pos)
            # print(" - Path: ", [f"{grid[p[1]][p[0]]} ({p})" for p in path])

            if grid[pos[1]][pos[0]] == 9:
                ends.add(pos)
                # print(" - Found end")
                return

            next_positions = find_next_valid_positions(pos)
            if not next_positions:
                return
            for next_pos in next_positions:
                find_path(next_pos, path + [next_pos])

        find_path(start, [start])
        return ends

    start_positions = []
    for y, row in enumerate(grid):
        for x, num in enumerate(row):
            if num == 0:
                start_positions.append((x, y))


    return sum([len(ends) for ends in [find_paths_from(start) for start in start_positions]])
    # for start in start_positions:
    #     print("Start: ", start)
    #     ends = find_paths_from(start)
    #     score = len(ends)
    #     print(score)




print("Part 1 test: ", part1(test_data))
print("Part 1 real: ", part1(real_data))
