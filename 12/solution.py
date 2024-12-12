# https://adventofcode.com/2024/day/12
from collections import deque

INPUT = "input"
TEST_INPUT = "test_input"

GardenType = list[list[str]]
PointType = tuple[int, int]


def find_regions(garden: GardenType, start: PointType):
    value = garden[start[1]][start[0]]
    width, height = len(garden[0]), len(garden)
    visited = set([start])
    area = 0
    perimeter = 0
    queue = deque([start])

    while queue:
        current = queue.popleft()
        if garden[current[1]][current[0]] == value:
            area += 1

        directions = (
            (current[0] - 1, current[1]),
            (current[0] + 1, current[1]),
            (current[0], current[1] - 1),
            (current[0], current[1] + 1),
        )
        for dir in directions:
            if not (0 <= dir[0] < width and 0 <= dir[1] < height):
                perimeter += 1
            elif garden[dir[1]][dir[0]] != value:
                perimeter += 1
            elif dir not in visited:
                visited.add(dir)
                queue.append(dir)

    return visited, area, perimeter


def count_corners(region_cells: set[PointType]) -> int:
    corners = 0
    for x, y in region_cells:
        outter = [
            ((x - 1, y), (x, y - 1)),
            ((x + 1, y), (x, y - 1)),
            ((x - 1, y), (x, y + 1)),
            ((x + 1, y), (x, y + 1)),
        ]
        inner = [(x - 1, y - 1), (x + 1, y - 1), (x - 1, y + 1), (x + 1, y + 1)]
        for (adj1, adj2), diag in zip(outter, inner):
            if adj1 not in region_cells and adj2 not in region_cells:
                corners += 1
            elif (
                adj1 in region_cells
                and adj2 in region_cells
                and diag not in region_cells
            ):
                corners += 1
    return corners


if __name__ == "__main__":
    with open(INPUT) as fp:
        content = [list(line.strip()) for line in fp.readlines()]

    garden = content
    price = 0
    seen = set()
    for y, row in enumerate(garden):
        for x, _ in enumerate(row):
            if (x, y) not in seen:
                region, area, perimeter = find_regions(garden, (x, y))
                seen.update(region)
                price += area * perimeter
    print("result", price)

    # part 2
    price = 0
    seen = set()
    for y, row in enumerate(garden):
        for x, _ in enumerate(row):
            if (x, y) not in seen:
                region, area, _ = find_regions(garden, (x, y))
                corners = count_corners(region)
                seen.update(region)
                price += area * corners
    print("result 2", price)
