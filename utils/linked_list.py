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
