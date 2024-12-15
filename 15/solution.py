# https://adventofcode.com/2024/day/15
from typing import Callable, Iterable
from copy import deepcopy


INPUT = "input"
TEST_INPUT = "test_input"
TEST_INPUT_2 = "test_input_2"

WALL = "#"
BOX = "O"
EMPTY = "."
ROBOT = "@"
BOX_WIDE = "[]"

LEFT = "<"
RIGHT = ">"
UP = "^"
DOWN = "v"

PointType = tuple[int, int]
LayoutType = list[list[str]]


MOVEMENTS: dict[str, Callable[[PointType], PointType]] = {
    LEFT: lambda pos: (pos[0] - 1, pos[1]),
    RIGHT: lambda pos: (pos[0] + 1, pos[1]),
    UP: lambda pos: (pos[0], pos[1] - 1),
    DOWN: lambda pos: (pos[0], pos[1] + 1),
}


class Wall(Exception):
    pass


def find_robot(layout: LayoutType) -> PointType:
    for y, row in enumerate(layout):
        for x, col in enumerate(row):
            if col == ROBOT:
                return (x, y)

    raise ValueError("No robot '@' found.")


def move(
    layout: LayoutType, pos: PointType, direction: Callable[[PointType], PointType]
) -> LayoutType:
    next_pos = direction(pos)
    next_pos_value = layout[next_pos[1]][next_pos[0]]
    if next_pos_value == WALL:
        raise Wall
    elif next_pos_value == BOX:
        layout = move(layout, next_pos, direction)
    layout[next_pos[1]][next_pos[0]] = layout[pos[1]][pos[0]]
    layout[pos[1]][pos[0]] = EMPTY
    return layout


def simulate(layout: LayoutType, commands: str, move_fn: Callable = move) -> LayoutType:
    robot = find_robot(layout)
    for command in commands:
        direction = MOVEMENTS[command]
        try:
            layout = move_fn(layout, robot, direction)
        except Wall:
            continue
        robot = direction(robot)
    return layout


def display_layout(layout: LayoutType) -> None:
    for row in layout:
        print("".join(row))


def box_sum(layout: LayoutType) -> int:
    result = 0
    y_mul = 100
    for y, row in enumerate(layout):
        for x, col in enumerate(row):
            if col == BOX:
                result += (y * y_mul) + x
    return result


def widden_layout(content: list[str]) -> Iterable[str]:
    for line in content:
        yield (
            line.replace(WALL, WALL * 2)
            .replace(EMPTY, EMPTY * 2)
            .replace(BOX, BOX_WIDE)
            .replace(ROBOT, ROBOT + EMPTY)
        )


def move_wide(
    layout: LayoutType, pos: PointType, direction: Callable[[PointType], PointType]
) -> LayoutType:
    layout = deepcopy(layout)
    next_pos = direction(pos)
    next_pos_value = layout[next_pos[1]][next_pos[0]]
    if next_pos_value == WALL:
        raise Wall
    elif next_pos_value in BOX_WIDE:
        if direction == MOVEMENTS[DOWN] or direction == MOVEMENTS[UP]:
            # add the otherside of the box to the compute tree
            if next_pos_value == BOX_WIDE[0]:
                layout = move_wide(layout, MOVEMENTS[RIGHT](next_pos), direction)
            else:
                layout = move_wide(layout, MOVEMENTS[LEFT](next_pos), direction)
        layout = move_wide(layout, next_pos, direction)
    layout[next_pos[1]][next_pos[0]] = layout[pos[1]][pos[0]]
    layout[pos[1]][pos[0]] = EMPTY

    return layout


def box_sum_wide(layout: LayoutType) -> int:
    result = 0
    y_mul = 100
    for y, row in enumerate(layout):
        for x, col in enumerate(row):
            if col == BOX_WIDE[0]:
                result += (y * y_mul) + x
    return result


if __name__ == "__main__":
    with open(INPUT) as fp:
        content = [line.strip() for line in fp.readlines()]

    split = content.index("")
    layout = [list(row) for row in content[:split]]
    display_layout(layout)
    moves = "".join(content[split + 1 :])
    res_layout = simulate(layout, moves)
    display_layout(res_layout)
    print("result", box_sum(res_layout))

    # part 2
    layout = [list(row) for row in widden_layout(content[:split])]
    display_layout(layout)
    res_layout = simulate(layout, moves, move_fn=move_wide)
    display_layout(res_layout)
    print("result 2", box_sum_wide(res_layout))
