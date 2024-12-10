import unittest

real_data = open("input.txt").read()


def parse(text):
    result = []
    file_id = 0
    for idx, char in enumerate(text):
        is_file = idx % 2 == 0
        block_count = int(char)
        if is_file and block_count > 0:
            result.append({"block_count": block_count, "is_file": True, "file_label": file_id})
        else:
            result.extend([{"is_file": False}] * block_count)

        if is_file:
            file_id += 1
    return result


def get_sum(blocks):
    result = 0
    idx = 0
    for element in blocks:
        if element['is_file']:
            for _ in range(element['block_count']):
                result += element['file_label'] * idx
                idx += 1
    return result


def part1(text):
    blocks = parse(text)
    while True:
        file_indices = [i for i, block in enumerate(blocks) if block["is_file"]]
        last_file_pos = file_indices[-1] if file_indices else None
        first_free_pos = next((idx for idx, block in enumerate(blocks) if not block["is_file"]), None)
        if first_free_pos is None or first_free_pos >= last_file_pos:
            break

        # create number node to add to beginning
        new_block_to_add = {
            "block_count": 1,
            "is_file": True,
            "file_label": blocks[last_file_pos]["file_label"]
        }

        # handle last digit
        if blocks[last_file_pos]['block_count'] > 1:
            blocks[last_file_pos]['block_count'] -= 1
        else:
            del blocks[last_file_pos]

        # replace empty block in beginning with a shorter block
        blocks[first_free_pos] = new_block_to_add

    return get_sum(blocks)


class Test(unittest.TestCase):
    def test_part1_test(self):
        self.assertEqual(part1("12345"), 60)
        self.assertEqual(part1("2333133121414131402"), 1928)
        self.assertEqual(part1("111111111111111111111"), 290)
        self.assertEqual(part1("10101010101010101010101"), 506)
        self.assertEqual(part1("1010101010101010101010"), 385)

    def test_part1_real(self):
        self.assertEqual(part1(real_data), 6337921897505)

