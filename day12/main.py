from collections import namedtuple

test_data = """RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE"""

real_data = open("input.txt").read()

Point = namedtuple("Point", ["x", "y"])
Region = namedtuple("Region", ["plant", "points"])

directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]


def find_regions(text):
    cols_by_rows = [list(row) for row in text.split("\n")]

    plants_by_points = {}

    for y in range(len(cols_by_rows)):
        for x in range(len(cols_by_rows[y])):
            plant = cols_by_rows[y][x]
            point = Point(x, y)
            plants_by_points[point] = plant

    unassigned_queue = list(plants_by_points.keys())
    regions = []
    visited = set()

    def dfs_collect_region(point, region, level=0):
        visited.add(point)
        if (point.x, point.y) in unassigned_queue:
            unassigned_queue.remove((point.x, point.y))
        region.points.add(point)
        val = plants_by_points.get(point)
        for dx, dy in directions:
            if dx == 0 and dy == 0:
                continue
            new_point = Point(point.x + dx, point.y + dy)
            new_val = plants_by_points.get(new_point, None)
            if new_val is not None and new_point not in visited:
                if new_val == val:
                    dfs_collect_region(new_point, region, level + 1)

    while unassigned_queue:
        region = Region(plants_by_points.get(unassigned_queue[0]), set())
        regions.append(region)
        dfs_collect_region(unassigned_queue[0], region)
    return regions, plants_by_points


def part1(text):
    regions, plants_by_points = find_regions(text)

    # find shared edges
    shared_edges_by_point = {}
    for point, plant in plants_by_points.items():
        shared_edges = 0
        for dx, dy in directions:
            new_point = Point(point.x + dx, point.y + dy)
            new_plant = plants_by_points.get(new_point, None)
            if new_plant is not None and new_plant == plant:
                shared_edges += 1
        shared_edges_by_point[point] = shared_edges

    def get_region_price(region):
        area = len(region.points)
        perimeter = 0
        for point in region.points:
            shared_edges = shared_edges_by_point[point]
            perimeter += 4 - shared_edges
        return area * perimeter

    return sum([get_region_price(region) for region in regions])


def part2(text):
    regions, plants_by_points = find_regions(text)

    def count_corners(region):
        corners = 0

        for x, y in region.points:
            pairs = [
                ((0, 1), (1, 0)),  # up, right
                ((1, 0), (0, -1)),  # right, down
                ((0, -1), (-1, 0)),  # down, left
                ((-1, 0), (0, 1))  # left, up
            ]
            for d1, d2 in pairs:
                first_in = (x + d1[0], y + d1[1]) in region.points
                second_in = (x + d2[0], y + d2[1]) in region.points

                is_outside_corner = (not first_in and not second_in)

                diagonal = (x + d1[0] + d2[0], y + d1[1] + d2[1])
                is_inside_corner = first_in and second_in and diagonal not in region.points

                if is_outside_corner or is_inside_corner:
                    corners += 1
        return corners

    def get_region_price(region):
        area = len(region.points)
        corner_count = count_corners(region)
        return area * corner_count

    return sum([get_region_price(region) for region in regions])


print("Part 1 test: ", part1(test_data))
print("Part 1 real: ", part1(real_data))
print("Part 2 test: ", part2(test_data))
print("Part 2 real: ", part2(real_data))