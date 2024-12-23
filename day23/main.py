from collections import namedtuple

test_data = """kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn"""


real_data = open("input.txt").read()

def part1(text):
    computers = {}
    for line in text.split("\n"):
        c1, c2 = line.split("-")
        if c1 not in computers:
            computers[c1] = set([])
        if c2 not in computers:
            computers[c2] = set([])
        computers[c1].add(c2)
        computers[c2].add(c1)

    def are_3_linked(c1, c2, c3):
        return (
                c1 in computers[c2] and c1 in computers[c3] and
                c2 in computers[c1] and c2 in computers[c3] and
                c3 in computers[c1] and c3 in computers[c2]
                )

    three_pairs = set([])
    for c1 in computers.keys():
        for c2 in computers[c1]:
            for c3 in computers[c2]:
                if are_3_linked(c1, c2, c3):
                    if c1.startswith('t') or c2.startswith('t') or c3.startswith('t'):
                        three_pairs.add(",".join(sorted([c1, c2, c3])))

    return len(three_pairs)




print("Part 1 test: ", part1(test_data))
print("Part 1 real: ", part1(real_data))
# print("Part 2 test: ", part2(test_data))
# print("Part 2 real: ", part2(real_data))
