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
    cols_by_rows = [list(row) for row in text.split("\n")]
    num_of_rows = len(cols_by_rows)
    num_of_columns = len(cols_by_rows[0])

    def detect_x_mas(x, y):
        if x < 1 or x == num_of_columns - 1 or y < 1 or y == num_of_rows - 1:
            return 0
        top_left = cols_by_rows[y - 1][x - 1]
        top_right = cols_by_rows[y - 1][x + 1]
        bottom_left = cols_by_rows[y + 1][x - 1]
        bottom_right = cols_by_rows[y + 1][x + 1]

        diag1 = top_left + "A" + bottom_right
        diag2 = top_right + "A" + bottom_left

        if (diag1 == "MAS" or diag1 == "SAM") and (diag2 == "MAS" or diag2 == "SAM"):
            return 1
        return 0

    x_mas_count = 0
    for y in range(num_of_rows):
        for x in range(num_of_columns):
            if cols_by_rows[y][x] == "A":
                x_mas_count += detect_x_mas(x, y)

    return x_mas_count


print("Part 1 test: ", part1(test_data))
print("Part 1 real: ", part1(real_data))
print("Part 2 test: ", part2(test_data))
print("Part 2 real: ", part2(real_data))
