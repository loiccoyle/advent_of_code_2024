# https://adventofcode.com/2024/day/8
from collections import defaultdict
from itertools import combinations
from typing import Iterable

INPUT = "input"
TEST_INPUT = "test_input"

PointType = tuple[int, int]


def get_antinodes(a: PointType, b: PointType) -> tuple[PointType, PointType]:
    delta_x = b[0] - a[0]
    delta_y = b[1] - a[1]
    return ((a[0] - delta_x, a[1] - delta_y), (b[0] + delta_x, b[1] + delta_y))


def get_resonant_antinodes(
    a: PointType, b: PointType, max_width: int, max_height: int
) -> Iterable[PointType]:
    delta_x = b[0] - a[0]
    delta_y = b[1] - a[1]

    # not very elegant but it works...
    # nicer way is to compute the left most point and go until the right most point
    start = b
    while 0 <= start[0] < max_width and 0 <= start[1] < max_height:
        yield start
        start = start[0] + delta_x, start[1] + delta_y
    start = a
    while 0 <= start[0] < max_width and 0 <= start[1] < max_height:
        yield start
        start = start[0] - delta_x, start[1] - delta_y


if __name__ == "__main__":
    antennas: dict[str, list[PointType]] = defaultdict(list)
    with open(INPUT) as fp:
        content = [line.strip() for line in fp.readlines()]

    map_width, map_height = len(content[0]), len(content)
    for y, line in enumerate(content):
        for x, char in enumerate(line.strip()):
            if char != ".":
                antennas[char].append((x, y))

    antinodes = set()
    for char, coords in antennas.items():
        for p1, p2 in combinations(coords, 2):
            for node in get_antinodes(p1, p2):
                if 0 <= node[0] < map_width and 0 <= node[1] < map_height:
                    antinodes.add(node)
    print("result", len(antinodes))

    # part 2
    antinodes = set()
    for char, coords in antennas.items():
        for p1, p2 in combinations(coords, 2):
            for node in get_resonant_antinodes(p1, p2, map_width, map_height):
                antinodes.add(node)
    print("result 2", len(antinodes))
