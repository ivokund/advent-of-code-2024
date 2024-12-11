test_data = "125 17"
real_data = "337 42493 1891760 351136 2 6932 73 0"


def part1(text, blink_count):
    stones = list(map(int, text.split()))

    stones_map = {}
    for stone in stones:
        stones_map[stone] = 1 + (stones_map[stone] if stone in stones_map else 0)

    def blink():
        nonlocal stones_map
        updates = {}

        def inc(value, by):
            updates[value] = by + (updates[value] if value in updates else 0)

        for stone, count in stones_map.items():
            string_val = str(stone)
            inc(stone, -count)
            if stone == 0:
                inc(1, count)
            elif len(string_val) % 2 == 0:
                first_value, second_value = int(string_val[:len(string_val)//2]), int(string_val[len(string_val)//2:])
                inc(first_value, count)
                inc(second_value, count)
            else:
                inc(stone * 2024, count)

        for stone, by in updates.items():
            if stone in stones_map:
                stones_map[stone] += by
            else:
                stones_map[stone] = by
            if stones_map[stone] == 0:
                del stones_map[stone]

    for i in range(blink_count):
        blink()

    return sum(list(stones_map.values()))


print("Part 1 test: ", part1(test_data, 25))
print("Part 1 real: ", part1(real_data, 25))
print("Part 2 test: ", part1(test_data, 75))
print("Part 2 real: ", part1(real_data, 75))
