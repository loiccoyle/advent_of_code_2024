# https://adventofcode.com/2024/day/13
import re

import numpy as np

INPUT = "input"
TEST_INPUT = "test_input"

PointType = tuple[int, int]


class Machine:
    def __init__(
        self,
        button_a: PointType,
        button_b: PointType,
        prize: PointType,
    ):
        self.button_matrix = [[button_a[0], button_b[0]], [button_a[1], button_b[1]]]
        self.prize_matrix = [prize[0], prize[1]]
        self.cost = [3, 1]

    def solve(
        self,
        prize_offset: int = 0,
    ):
        prize_matrix = np.array(self.prize_matrix) + prize_offset
        solution = np.linalg.solve(self.button_matrix, prize_matrix)
        if np.all(np.isclose(solution - solution.round(), 0, atol=1e-3)):
            return int((solution.round() * self.cost).sum())
        return 0


def parse_machines(content: str) -> list[Machine]:
    button_a_pattern = re.compile(r"Button A: X\+(\d*), Y\+(\d*)")
    button_b_pattern = re.compile(r"Button B: X\+(\d*), Y\+(\d*)")
    prize_pattern = re.compile(r"Prize: X=(\d*), Y=(\d*)")
    return [
        Machine(button_a, button_b, prize)
        for (button_a, button_b, prize) in zip(
            ((int(x), int(y)) for x, y in re.findall(button_a_pattern, content)),
            ((int(x), int(y)) for x, y in re.findall(button_b_pattern, content)),
            ((int(x), int(y)) for x, y in re.findall(prize_pattern, content)),
        )
    ]


if __name__ == "__main__":
    with open(INPUT) as fp:
        content_raw = fp.read()

    machines = parse_machines(content_raw)
    print("result", sum([machine.solve() for machine in machines]))

    # part 2
    print(
        "result 2",
        sum([machine.solve(prize_offset=10000000000000) for machine in machines]),
    )
