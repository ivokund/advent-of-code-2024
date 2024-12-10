test_data = "2333133121414131402"
real_data = open("input.txt").read()


def parse(text):
    result = []
    file_id = 0
    for idx, char in enumerate(text):
        is_file = idx % 2 == 0
        block_count = int(char)
        if is_file and block_count > 0:
            result.append({"block_count": block_count, "is_file": True, "file_label": file_id})
        elif block_count > 0:
            result.extend([{"is_file": False, "block_count": block_count}])

        if is_file:
            file_id += 1
    return result


def get_sum(blocks):
    result = 0
    idx = 0
    for element in blocks:
        if element['is_file']:
            for _ in range(element['block_count']):
                # print("-- adding sum ({} x {}) = {}".format(element['file_label'], idx, element['file_label'] * idx))
                result += element['file_label'] * idx
                idx += 1
        else:
            idx += element['block_count']
    return result


def draw(file):
    result = ""
    for element in file:
        if element['is_file']:
            result += "" + str(element['file_label']) * element['block_count'] + ""
        else:
            result += "" + '.' * element['block_count'] + ""
    print(result)
    print("")


def part2(text):
    blocks = parse(text)
    # print(blocks)
    right_ignore_index = float('inf')
    while True:
        file_indices = [i for i, block in enumerate(blocks) if block["is_file"] and i < right_ignore_index]
        if len(file_indices) == 0:
            break
        last_file_pos = file_indices[-1]

        first_free_pos = next((
            idx for idx, block in enumerate(blocks) if (
               not block["is_file"]
               and block['block_count'] >= blocks[last_file_pos]['block_count']
               and idx < right_ignore_index
            )), None)

        if first_free_pos is None or first_free_pos >= last_file_pos:
            right_ignore_index = last_file_pos
            continue

        remaining_space = blocks[first_free_pos]['block_count'] - blocks[last_file_pos]['block_count'] # need add this back

        blocks[first_free_pos]['block_count'] = blocks[last_file_pos]['block_count']
        blocks[first_free_pos], blocks[last_file_pos] = blocks[last_file_pos], blocks[first_free_pos]

        if remaining_space > 0:
            blocks.insert(first_free_pos + 1, {"is_file": False, "block_count": remaining_space})
            right_ignore_index += 1

    return get_sum(blocks)


print("Part 2 test: ", part2(test_data))
print("Part 2 real: ", part2(real_data))
