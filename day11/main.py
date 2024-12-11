test_data = "125 17"
real_data = "337 42493 1891760 351136 2 6932 73 0"

class List:
    def __init__(self, stones):
        self.head = None
        for stone in stones:
            self.insert_at_beginning(stone)

    def __str__(self):
        head = self.head
        out = "HEAD: "
        while head:
            out += str(head) + "  --->  "
            head = head.next
        return out

    def draw(self):
        print(str(self))

    def count(self):
        head = self.head
        count = 0
        while head:
            count += 1
            head = head.next
        return count

    def insert_at_beginning(self, value):
        new_node = Node(value)
        new_node.next = self.head
        prev_head = self.head
        self.head = new_node
        if prev_head:
            prev_head.prev = new_node

    def replace_with_two(self, node, node1, node2):
        new_node_1 = Node(node2)
        new_node_2 = Node(node1)

        new_node_1.next, new_node_2.prev = new_node_2, new_node_1
        new_node_2.next = node.next

        if node.prev is None: # it's head
            self.head = new_node_1
        else:
            new_node_1.prev = node.prev
            node.prev.next = new_node_1

        if node.next:
            node.next.prev = new_node_2

        node.prev, node.next = None, None
        # print(" ---- node after", node)
        # print(" ---- new_node_1", new_node_1)
        # print(" ---- new_node_2", new_node_2)
        return new_node_1, new_node_2

class Node:
    def __init__(self, value):
        # Initialize a new node with data, previous, and next pointers
        self.value = value
        self.next = None
        self.prev = None

    def __str__(self):
        # prev_val = self.prev.value if self.prev else None
        # next_val = self.next.value if self.next else None
        # return "{} < ({}) > {}".format(prev_val, self.value, next_val)
        return "{}<-({})->{}".format(
            self.prev.value if self.prev else 'X',
            self.value,
            self.next.value if self.next else 'X'
        )


def part1(text, blink_count):
    stones = list(map(int, text.split()))

    linked_list = List(stones)
    # print(" == list done, start ==\n")
    # linked_list.draw()

    # stones_map = {}
    # for stone in stones:
    #     stones_map[stone] = 1 + (stones_map[stone] if stone in stones_map else 0)
    #
    # print(stones_map)

    def blink():
        # print('\n\n === STARTING BLINK ===')
        # linked_list.draw()
        current = linked_list.head
        while current:
            # print("\n -- CURRENT ====: ", current)
            string_val = str(current.value)
            # print(" -- string_val: ", string_val)
            if current.value == 0:
                # print(" - zero")
                current.value = 1
                current = current.next
            elif len(string_val) % 2 == 0:
                # print(" - splitting")
                first_value, second_value = int(string_val[:len(string_val)//2]), int(string_val[len(string_val)//2:])
                # print(" - first_value: ", first_value)
                # print(" - second_value: ", second_value)
                first, second = linked_list.replace_with_two(current, first_value, second_value)
                # print('@@@@ SPLIT DONE')
                # print(' - first', first)
                # print(' - second', second)
                current = second.next
            else:
                # print(" - multiplying")
                current.value *= 2024
                current = current.next
            # print(" - loop complete")
            # linked_list.draw()
        return None

    for i in range(blink_count):
        print("blinked: ", i)
        print("count", linked_list.count())
        blink()
    return linked_list.count()



# print("Part 1 test: ", part1(test_data, 25))
# print("Part 1 real: ", part1(real_data, 25))
print("Part 2 test: ", part1(test_data, 75))
# print("Part 2 real: ", part1(real_data, 75))
