# test_data = """010"""
# test_data = """12345"""
test_data = """2333133121414131402""" # 1928
# test_data = """10101010101010101010101""" # 503
# test_data = """111111111111111111111""" # 290
# test_data = """1010101010101010101010""" # 385

real_data = open("input.txt").read()


def parse(text):
    result = []
    file_id = 0
    for idx, char in enumerate(text):
        is_file = idx % 2 == 0
        block_count = int(char)
        if is_file and block_count > 0: ## ???
            result.append({
                "block_count": block_count,
                "is_file": True,
                "file_label": file_id
            })
        else:
            result.extend([{"is_file": False}] * block_count)

        if is_file:
            file_id += 1
    return result


def part1(text):
    blocks = parse(text)

    def get_sum(blocks):
        result = 0
        idx = 0
        for element in blocks:
            if element['is_file']:
                for _ in range(element['block_count']):
                    # print("-- adding sum ({} x {}) = {}".format(element['file_label'], idx, element['file_label'] * idx))
                    result += element['file_label'] * idx
                    idx += 1
        return result

    def draw(file):
        result = ""
        for element in file:
            if element['is_file']:
                result += "(" + str(element['file_label']) * element['block_count'] + ")"
            else:
                result += "."
        print(result)
        print("")
    #
    # print(blocks)
    # draw(blocks)
    # print("sum", get_sum(blocks))
    # exit(0)


    while True:
        # print("== LOOP ==")
        # print(blocks)
        # print(" start:")
        # draw(blocks)
        file_indices = [i for i, block in enumerate(blocks) if block["is_file"]]
        last_file_pos = file_indices[-1] if file_indices else None
        # print("- last_file_pos", last_file_pos)
        first_free_pos = next((idx for idx, block in enumerate(blocks) if not block["is_file"]), None)
        # print("- first_free_pos", first_free_pos)
        if first_free_pos is None or first_free_pos >= last_file_pos:
            # print(" - breaking")
            break

        # create number node to add to beginning
        new_block_to_add = {
            "block_count": 1,
            "is_file": True,
            "file_label": blocks[last_file_pos]["file_label"]
        }
        # print("- new_block_to_add", new_block_to_add)

        # handle last digit
        if blocks[last_file_pos]['block_count'] > 1:
            blocks[last_file_pos]['block_count'] -= 1
            # print("- decremented")
        else:
            del blocks[last_file_pos]
            # print("- deleted")

        # replace empty block in beginning with a shorter block
        blocks[first_free_pos] = new_block_to_add

        # print("- end")
        # draw(blocks)

    # print("end")
    draw(blocks)
    return get_sum(blocks)


print("Part 1 test: ", part1(test_data))
print("Part 1 real: ", part1(real_data))
# print("Part 2 test: ", part2(test_data))
# print("Part 2 real: ", part2(real_data))

# wrong 90095094087
# wrong 85447704075, 85535077891, 85535077891
# wrong 2735004463647223305301935318131716490526069
