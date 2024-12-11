# https://adventofcode.com/2024/day/10
from collections import deque

INPUT = "input"
TEST_INPUT = "test_input"

PointType = tuple[int, int]


def trailhead_score(trail_map: list[list[int]], start: PointType) -> int:
    visited: set[PointType] = set()
    score = 0
    width, height = len(trail_map[0]), len(trail_map)
    queue = deque([start])
    while queue:
        head = queue.popleft()
        if head in visited:
            continue
        visited.add(head)
        head_height = trail_map[head[1]][head[0]]
        if head_height == 9:
            score += 1
            continue

        directions = (
            (head[0] - 1, head[1]),
            (head[0] + 1, head[1]),
            (head[0], head[1] - 1),
            (head[0], head[1] + 1),
        )
        for direction in directions:
            if (
                0 <= direction[0] < width
                and 0 <= direction[1] < height
                and trail_map[direction[1]][direction[0]] == head_height + 1
            ):
                queue.append(direction)
    return score


def trailhead_rating(trail_map: list[list[int]], start: PointType) -> int:
    score = 0
    width, height = len(trail_map[0]), len(trail_map)
    queue = deque([start])
    while queue:
        head = queue.popleft()
        head_height = trail_map[head[1]][head[0]]
        if head_height == 9:
            score += 1
            continue

        directions = (
            (head[0] - 1, head[1]),
            (head[0] + 1, head[1]),
            (head[0], head[1] - 1),
            (head[0], head[1] + 1),
        )
        for direction in directions:
            if (
                0 <= direction[0] < width
                and 0 <= direction[1] < height
                and trail_map[direction[1]][direction[0]] == head_height + 1
            ):
                queue.append(direction)
    return score


if __name__ == "__main__":
    with open(INPUT) as fp:
        content = [list(map(int, line.strip())) for line in fp.readlines()]

    print(content)
    score = 0
    for y, row in enumerate(content):
        for x, height in enumerate(row):
            if height == 0:
                score += trailhead_score(content, (x, y))
    print("result", score)

    # part 2
    score = 0
    for y, row in enumerate(content):
        for x, height in enumerate(row):
            if height == 0:
                score += trailhead_rating(content, (x, y))
    print("result 2", score)
