test_data = """MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX"""
real_data = open("input.txt").read()


def part1(text):
    cols_by_rows = [list(row) for row in text.split("\n")]

    num_of_rows = len(cols_by_rows)
    num_of_columns = len(cols_by_rows[0])

    def read_diagonal(from_x, from_y, dx):
        x, y = from_x, from_y
        result = ""
        while num_of_rows > x >= 0 and y < num_of_columns:
            result += cols_by_rows[y][x]
            x += dx
            y += 1
        return result

    horizontals = ["".join(row) for row in cols_by_rows]
    verticals = []
    diagonals_right = []
    diagonals_left = []
    for x in range(num_of_rows):
        verticals.append("".join(row[x] for row in cols_by_rows))
        for y in range(num_of_columns):
            if x == 0 or y == 0:
                diagonals_right.append(read_diagonal(x, y, 1))
            if x == num_of_rows - 1 or y == 0:
                diagonals_left.append(read_diagonal(x, y, -1))

    strings = " ".join(horizontals + verticals + diagonals_right + diagonals_left)
    all_strings = strings + " " + strings[::-1]
    return all_strings.count("XMAS")

def part2(text):
    pass



print("Part 1 test: ", part1(test_data))
print("Part 1 real: ", part1(real_data))
# print("Part 2 test: ", part2(test_data))
# print("Part 2 real: ", part2(real_data))
