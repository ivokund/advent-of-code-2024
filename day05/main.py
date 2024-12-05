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


def breaks_any_rule(rules, number, list_before, list_after):
    def breaks_rule(rule):
        if rule[0] == number:  # rule[1] must not be present in list_before
            return rule[1] in list_before
        if rule[1] == number:  # rule[0] must not be present in list_after
            return rule[0] in list_after
        return False
    return any(breaks_rule(rule) for rule in rules)


def get_valid_and_invalid(rules, updates):
    def update_breaks_any_rule(update):
        for i, number in enumerate(update):
            if breaks_any_rule(rules, number, update[:i], update[i+1:]):
                return True
        return False
    incorrect_updates = [update for update in updates if update_breaks_any_rule(update)]
    correct_updates = [update for update in updates if update not in incorrect_updates]
    return correct_updates, incorrect_updates


def get_middle_element(update):
    count = len(update)
    return update[count // 2]


def part1(text):
    rules, updates = parse(text)
    correct_updates, _ = get_valid_and_invalid(rules, updates)
    middles = [get_middle_element(update) for update in correct_updates]

    return sum(middles)

def part2(text):
    rules, updates = parse(text)
    _, incorrect_updates = get_valid_and_invalid(rules, updates)

    def sort_update(update):
        used_rules = list(filter(lambda rule: rule[0] in update and rule[1] in update, rules))
        print("used rules", list(used_rules))
        print("update", update)

        last_number = next(num for num in update if num not in [rule[0] for rule in used_rules])
        print("last", last_number)
        stack = update.copy()
        stack.remove(last_number)
        sorted_update = [last_number]
        while len(stack) > 0:
            print("=== INSIDE LOOP ===")
            print("-- stack", stack)
            first_element = sorted_update[0]
            print("-- first", first_element)
            # find candidates of used rules that have first_element as its last element
            candidates = [rule[0] for rule in used_rules if rule[1] == first_element]
            print("-- candidates", candidates)
            correct_candidates = [candidate for candidate in candidates if not
                                  breaks_any_rule(
                                      used_rules,
                                      candidate,
                                      [x for x in stack if x != candidate],
                                      sorted_update
                                  )]
            print("-- correct candidates", list(correct_candidates))
            if len(correct_candidates) != 1:
                raise Exception("Incorrect number of correct candidates")

            stack.remove(correct_candidates[0])
            sorted_update = correct_candidates + sorted_update
        return sorted_update

    updates = [sort_update(update) for update in incorrect_updates]
    middles = [get_middle_element(update) for update in updates]
    return sum(middles)


# print("Part 1 test: ", part1(test_data))
# print("Part 1 real: ", part1(real_data))
print("Part 2 test: ", part2(test_data))
print("Part 2 real: ", part2(real_data))
