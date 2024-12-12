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


def part1(text):
    cols_by_rows = [list(row) for row in text.split("\n")]

    regions_by_plant = {}
    plants_by_points = {}




    for y in range(len(cols_by_rows)):
        for x in range(len(cols_by_rows[y])):
            plant = cols_by_rows[y][x]
            point = Point(x, y)
            plants_by_points[point] = plant

    # find shared edges
    shared_edges_by_point = {}
    for point, plant in plants_by_points.items():
        shared_edges = 0
        deltas = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dx, dy in deltas:
            new_point = Point(point.x + dx, point.y + dy)
            new_plant = plants_by_points.get(new_point, None)
            if new_plant is not None and new_plant == plant:
                shared_edges += 1
        shared_edges_by_point[point] = shared_edges



    unassigned_queue = list(plants_by_points.keys())
    regions = []
    visited = set()
    def dfs_collect_region(point, region, level=0):
        visited.add(point)
        if (point.x, point.y) in unassigned_queue:
            unassigned_queue.remove((point.x, point.y))
        region.points.add(point)
        val = plants_by_points.get(point)
        deltas = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dx, dy in deltas:
            if dx == 0 and dy == 0:
                continue
            new_point = Point(point.x + dx, point.y + dy)
            new_val = plants_by_points.get(new_point, None)
            if new_val is not None and new_point not in visited:
                if new_val == val:
                    dfs_collect_region(new_point, region, level + 1)

    while unassigned_queue:
        # print("\n\n==== RUNNING QUEUE START FROM ", unassigned_queue[0])
        region = Region(plants_by_points.get(unassigned_queue[0]), set())
        regions.append(region)
        dfs_collect_region(unassigned_queue[0], region)

    def get_region_price(region):
        area = len(region.points)
        perimeter = 0
        for point in region.points:
            shared_edges = shared_edges_by_point[point]
            perimeter += 4 - shared_edges
        return area * perimeter

    return sum([get_region_price(region) for region in regions])


print("Part 1 test: ", part1(test_data))
print("Part 1 real: ", part1(real_data))
# print("Part 2 test: ", part2(test_data))
# print("Part 2 real: ", part2(real_data))