import unittest

test_data = """1
10
100
2024"""


real_data = open("input.txt").read()


def prune(num: int) -> int:
    return num % 16777216


def mix(value: int, secret: int) -> int:
    return value ^ secret


def evolve(secret: int) -> int:
    secret = prune(mix(secret * 64, secret))
    secret = prune(mix(secret // 32, secret))
    return prune(mix(secret * 2048, secret))


def simulate_to(secret: int, count: int) -> int:
    for _ in range(count):
        secret = evolve(secret)
    return secret


def part1(text):
    numbers = list(map(int, text.split("\n")))
    return sum([simulate_to(num, 2000) for num in numbers])


class OperationsTest(unittest.TestCase):
    def test_prune(self):
        self.assertEqual(prune(100000000), 16113920)

    def test_mix(self):
        self.assertEqual(mix(15, 42), 37)

    def test_evolve(self):
        self.assertEqual(evolve(123), 15887950)

    def test_simulate_to(self):
        self.assertEqual(simulate_to(123, 10), 5908254)

    def test_part1(self):
        self.assertEqual(part1(test_data), 37327623)
        self.assertEqual(part1(real_data), 17163502021)

