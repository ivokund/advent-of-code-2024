import math
import re
from collections import namedtuple
from functools import reduce
from operator import mul

test_data = """p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3"""

# test_data = "p=2,4 v=2,-3"

real_data = open("input.txt").read()

Movement = namedtuple("Movement", ["dx", "dy"])
Point = namedtuple("Point", ["x", "y"])
Robot = namedtuple("Robot", ["pos", "movement"])


def parse_input(text):
    parts = [
        [
            [[int(num) for num in subpart.split(",") if num.lstrip('-').isnumeric()]
                for subpart in part.split("=") if len(subpart) > 1][0]
            for part in line.split(" ")
        ][:2]
        for line in text.split("\n")
    ]
    return [Robot(Point(*part[0]), Movement(*part[1])) for part in parts]


def draw(robots, grid_size):
    counts_by_coords = {}
    for robot in robots:
        if robot.pos in counts_by_coords:
            counts_by_coords[robot.pos] += 1
        else:
            counts_by_coords[robot.pos] = 1
    for y in range(grid_size[1]):
        for x in range(grid_size[0]):
            if Point(x, y) in counts_by_coords:
                print(counts_by_coords[Point(x, y)], end="")
            else:
                print(".", end="")
        print("")
    print("\n")




def part1(text, grid_size):
    robots = parse_input(text)

    def move(robots):
        grid_x, grid_y = grid_size
        def get_next_pos(robot):
            new_x = (robot.pos.x + robot.movement.dx) % grid_x
            new_y = (robot.pos.y + robot.movement.dy) % grid_y
            return Point(
                (new_x + grid_x) % grid_x,
                (new_y + grid_y) % grid_y
            )
        return [Robot(get_next_pos(robot), robot.movement) for robot in robots]

    def count_by_quadrants(robots):
        width, height = grid_size[0], grid_size[1]
        quadrants = [
            ((0, width//2 - 1), (0, height//2 - 1)),  # top left
            ((width//2 + 1, width - 1), (0, height//2 - 1)),  # top right
            ((0, width//2 - 1), (height//2 + 1, height - 1)),  # bottom left
            ((width//2 + 1, width - 1), (height//2 + 1, height - 1)),  # bottom right
        ]
        counts = [0 for _ in range(4)]
        for robot in robots:
            for i, (x_range, y_range) in enumerate(quadrants):
                if x_range[0] <= robot.pos.x <= x_range[1] and y_range[0] <= robot.pos.y <= y_range[1]:
                    counts[i] += 1
        return counts

    for i in range(100):
        robots = move(robots)
        draw(robots, grid_size)

    counts = count_by_quadrants(robots)
    return reduce(mul, counts)


def part2(text, grid_size):


    def move(robots):
        min_max_by_y = {}

        grid_x, grid_y = grid_size
        def get_next_pos(robot):
            new_x = (robot.pos.x + robot.movement.dx) % grid_x
            new_y = (robot.pos.y + robot.movement.dy) % grid_y
            return Point(
                (new_x + grid_x) % grid_x,
                (new_y + grid_y) % grid_y
            )
        new_robots = []
        for robot in robots:
            new_pos = get_next_pos(robot)
            new_robots.append(Robot(new_pos, robot.movement))
            if new_pos.y not in min_max_by_y:
                min_max_by_y[new_pos.y] = (new_pos.x, new_pos.x)
            else:
                min_max_by_y[new_pos.y] = min(min_max_by_y[new_pos.y][0], new_pos.x), max(min_max_by_y[new_pos.y][0], new_pos.x)
        return new_robots, min_max_by_y

    def is_tree_like(robots, min_max_by_y):
        for y in min_max_by_y.keys():
            if min_max_by_y[y][0] == grid_size[0] - 1 - min_max_by_y[y][1]:
                print("Tree-like found at y=", y)
                # print(robots_by_y)
            else:
                return False

        draw(robots, grid_size)

    robots = parse_input(text)
    i = 0
    while True:
        i += 1
        if i % 1000 == 0:
            print("Second: ", i)
        robots, min_max_by_y = move(robots)
        # draw(robots, grid_size)
        # print(robots)
        # print("Min max by y: ", min_max_by_y)
        if is_tree_like(robots, min_max_by_y):
            break

    return i


# print("Part 1 test: ", part1(test_data, (7, 11)))
# print("Part 1 real: ", part1(real_data, (101, 103)))
# print("Part 2 test: ", part2(test_data, (7, 11)))
print("Part 2 real: ", part2(real_data, (101, 103)))

# wrong 98535360