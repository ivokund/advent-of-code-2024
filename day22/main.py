import unittest
from collections import defaultdict

test_data = """1
10
100
2024"""

test_data_2 = """1
2
3
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


def get_prices_per_sequence(secret, total_iterations):
    secrets = [secret]
    for _ in range(total_iterations-1):
        secrets.append(evolve(secrets[-1]))

    prices = [secret % 10 for secret in secrets]
    price_diffs = [None] + [prices[i] - prices[i - 1] for i in range(1, len(prices))]

    price_per_sequence = {}
    for idx in range(4, len(prices)):
        sequence_str = ",".join(map(str, price_diffs[idx-3:idx+1]))
        if sequence_str not in price_per_sequence:
            price_per_sequence[sequence_str] = prices[idx]

    return price_per_sequence


def part1(text):
    numbers = list(map(int, text.split("\n")))
    return sum([simulate_to(num, 2000) for num in numbers])


def part2(text):
    numbers = list(map(int, text.split("\n")))

    all_prices_per_sequence = defaultdict(int)

    for num in numbers:
        prices_per_sequence = get_prices_per_sequence(num, 2000)
        for sequence, price in prices_per_sequence.items():
            all_prices_per_sequence[sequence] += price

    return max(all_prices_per_sequence.values())


class Tests(unittest.TestCase):
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

    def test_get_sequences_per_price(self):
        prices = get_prices_per_sequence(123, 10)
        self.assertEqual(prices['-1,-1,0,2'], 6)

    def test_part2(self):
        self.assertEqual(part2(test_data_2), 23)
        self.assertEqual(part2(real_data), 1938)
