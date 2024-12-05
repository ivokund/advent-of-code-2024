test_data = """47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47"""
real_data = open("input.txt").read()

def parse(text):
    rules_txt, pages_txt = text.split("\n\n")
    rules = [[int(num) for num in rule.split("|")] for rule in rules_txt.split("\n")]
    updates = [[int(num) for num in page.split(",")] for page in pages_txt.split("\n")]
    return rules, updates


def part1(text):
    rules, updates = parse(text)

    def breaks_rule(rule, number, list_before, list_after):
        if rule[0] == number:  # rule[1] must not be present in list_before
            return rule[1] in list_before
        if rule[1] == number:  # rule[0] must not be present in list_after
            return rule[0] in list_after
        return False

    def breaks_any_rule(number, list_before, list_after):
        return any(breaks_rule(rule, number, list_before, list_after) for rule in rules)

    def update_breaks_any_rule(update):
        for i, number in enumerate(update):
            if breaks_any_rule(number, update[:i], update[i+1:]):
                return True
        return False

    def get_middle_element(update):
        count = len(update)
        return update[count // 2]

    correct_updates = filter(lambda update: not update_breaks_any_rule(update), updates)
    middles = [get_middle_element(update) for update in correct_updates]

    return sum(middles)


print("Part 1 test: ", part1(test_data))
print("Part 1 real: ", part1(real_data))
# print("Part 2 test: ", part2(test_data))
# print("Part 2 real: ", part2(real_data))
