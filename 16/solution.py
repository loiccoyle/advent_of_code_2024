# https://adventofcode.com/2024/day/16/
from collections import defaultdict
from heapq import heapify, heappop, heappush

INPUT = "input"
TEST_INPUT = "test_input"

WALL = "#"
START = "S"
EMPTY = "."
END = "E"

TURN_COST = 1000
STEP_COST = 1

MazeType = list[list[str]]
PointType = tuple[int, int]


# right, down, left, up
DIRECTIONS = [(1, 0), (0, 1), (-1, 0), (0, -1)]


def print_maze(maze: MazeType) -> None:
    for row in maze:
        print("".join(row))


def find_start(maze: MazeType) -> PointType:
    for y, row in enumerate(maze):
        for x, col in enumerate(row):
            if col == "S":
                return x, y
    raise ValueError("No start 'S' found.")


def traverse(maze: MazeType) -> int:
    start = find_start(maze)
    heap = [(0, start, 0)]
    heapify(heap)
    visited = set()

    while heap:
        score, pos, dir_i = heappop(heap)
        if (pos, dir_i) in visited:
            continue
        visited.add((pos, dir_i))

        if maze[pos[1]][pos[0]] == END:
            return score

        for dir_shift in range(-1, 2):
            new_dir_i = (dir_i + dir_shift) % 4
            dx, dy = DIRECTIONS[new_dir_i]
            neighbor = (pos[0] + dx, pos[1] + dy)

            if maze[neighbor[1]][neighbor[0]] == WALL:
                continue

            new_score = score + abs(dir_shift) * TURN_COST + STEP_COST
            heappush(heap, (new_score, neighbor, new_dir_i))

    return float("inf")  # type: ignore


def traverse_2(maze: MazeType) -> list[PointType]:
    start = find_start(maze)
    heap = [(0, start, 0, [start])]
    heapify(heap)
    # keep track of the best score at each tile, so that we can keep going if we're on
    # an optimal path we've already explored
    visited = defaultdict(lambda: float("inf"))
    best_tiles = []

    while heap:
        score, pos, dir_i, path = heappop(heap)

        # we seen this tile before with a better score (not on an optimal path)
        if (pos, dir_i) in visited and visited[(pos, dir_i)] < score:
            continue

        # update with the new best
        visited[(pos, dir_i)] = score

        if maze[pos[1]][pos[0]] == END:
            best_tiles.extend(path)
            continue

        for dir_shift in range(-1, 2):
            new_dir_i = (dir_i + dir_shift) % 4
            dx, dy = DIRECTIONS[new_dir_i]
            neighbor = (pos[0] + dx, pos[1] + dy)

            if maze[neighbor[1]][neighbor[0]] == WALL:
                continue

            new_score = score + abs(dir_shift) * TURN_COST + STEP_COST
            heappush(heap, (new_score, neighbor, new_dir_i, path + [neighbor]))

    return best_tiles


if __name__ == "__main__":
    with open(INPUT) as fp:
        maze = [list(line.strip()) for line in fp.readlines()]

    score = traverse(maze)
    print("result", score)

    paths = traverse_2(maze)
    print("result 2", len(set(paths)))
