from collections import namedtuple

test_data = """##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^"""


real_data = open("input.txt").read()

Point = namedtuple("Point", ["x", "y"])
Grid = namedtuple("Grid", ["width", "height", "robot", "boxes", "walls"])


def parse(text):
    map_text, movements_text = text.split("\n\n")
    movements = list(movements_text.replace("\n", ""))

    walls = set()
    boxes = set()
    robot = None
    lines = map_text.split("\n")
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char == "#":
                walls.add(Point(x, y))
            elif char == "@":
                robot = Point(x, y)
            elif char == "O":
                boxes.add(Point(x, y))

    return Grid(
        width=len(lines[0]),
        height=len(lines),
        robot=robot,
        boxes=boxes,
        walls=walls
    ), movements

def draw(grid):
    for y in range(grid.height):
        line = ""
        for x in range(grid.width):
            point = Point(x, y)
            if point == grid.robot:
                line += "@"
            elif point in grid.boxes:
                line += "O"
            elif point in grid.walls:
                line += "#"
            else:
                line += "."
        print(line)
    print("")

def part1(text):
    grid, movements = parse(text)

    draw(grid)

    def get_pos_from(point, movement):
        deltas = {
            "^": Point(0, -1),
            "v": Point(0, 1),
            "<": Point(-1, 0),
            ">": Point(1, 0)
        }
        return Point(point.x + deltas[movement].x, point.y + deltas[movement].y)

    def is_free(pos, grid):
        return pos not in grid.walls and pos not in grid.boxes

    def is_wall(pos, grid):
        return pos in grid.walls

    def is_box(pos, grid):
        return pos in grid.boxes

    def is_box_movable(pos, direction, grid):
        next_pos = get_pos_from(pos, direction)
        return is_free(next_pos, grid) or is_box(next_pos, grid) and is_box_movable(next_pos, direction, grid)

    def move_boxes_from(pos, movement, grid):
        # print("Starting move boxes from {} to {}".format(pos, movement))
        boxes_to_move = {pos}
        while True:
            # print("loop start")
            pos = get_pos_from(pos, movement)
            # print("pos", pos)
            if is_free(pos, grid):
                # print(" - is free")
                can_move = True
                break
            elif is_box(pos, grid):
                # print(" - is box")
                boxes_to_move.add(pos)
            else:
                # print(" - is wall")
                can_move = False
                break
        if can_move:
            # print(" - can move")
            # print("will move ", boxes_to_move)
            new_boxes = set([get_pos_from(box, movement) for box in boxes_to_move])
            # print("'a")
        else:
            new_boxes = boxes_to_move
            # print(" - can't move")
        # print(" - old boxes: ", boxes_to_move)
        # print(" - new boxes: ", new_boxes)
        return boxes_to_move, new_boxes

    def move(grid, movement):
        next_pos = get_pos_from(grid.robot, movement)

        if is_free(next_pos, grid):
            return Grid(
                width=grid.width,
                height=grid.height,
                robot=next_pos,
                boxes=grid.boxes,
                walls=grid.walls
            )
        elif is_wall(next_pos, grid):
            return grid
        elif is_box(next_pos, grid) and is_box_movable(next_pos, movement, grid):
            old_boxes, new_boxes = move_boxes_from(next_pos, movement, grid)

            # print("MOVE complete: ", old_boxes, new_boxes)
            return Grid(
                width=grid.width,
                height=grid.height,
                robot=next_pos,
                boxes=(grid.boxes - old_boxes) | new_boxes,
                walls=grid.walls
            )
        return grid

    for movement in movements:
        # print("Movement: ", movement)
        # print("BEFORE")
        # draw(grid)
        grid = move(grid, movement)
        # print("AFTER")
        # draw(grid)

    return sum([box.y * 100 + box.x for box in grid.boxes])


print("Part 1 test: ", part1(test_data))
print("Part 1 real: ", part1(real_data))

