# https://adventofcode.com/2024/day/6

INPUT = "input"
TEST_INPUT = "test_input"


def up(start: tuple[int, int]) -> tuple[int, int]:
    return start[0], start[1] - 1


def down(start: tuple[int, int]) -> tuple[int, int]:
    return start[0], start[1] + 1


def left(start: tuple[int, int]) -> tuple[int, int]:
    return start[0] - 1, start[1]


def right(start: tuple[int, int]) -> tuple[int, int]:
    return start[0] + 1, start[1]


DIRECTION_CYCLE = [up, right, down, left]


def find_start(content) -> tuple[int, int]:
    for y, row in enumerate(content):
        for x, col in enumerate(row):
            if col == "^":
                return x, y

    raise ValueError("No start '^' found.")


def find_obstacles(content) -> set[tuple[int, int]]:
    out = set()
    for y, row in enumerate(content):
        for x, col in enumerate(row):
            if col == "#":
                out.add((x, y))
    return out


def walk_map(
    obstacles: set[tuple[int, int]],
    start: tuple[int, int],
    max_x: int,
    max_y: int,
    direction_i: int = 0,
):
    direction_i %= 4
    (x, y) = start
    direction = DIRECTION_CYCLE[direction_i]
    (new_x, new_y) = direction((x, y))
    while 0 <= new_x < max_x and 0 <= new_y < max_y:
        if (new_x, new_y) in obstacles:
            direction_i = (direction_i + 1) % 4
            direction = DIRECTION_CYCLE[direction_i]
        else:
            x, y = new_x, new_y
            yield x, y, direction_i
        (new_x, new_y) = direction((x, y))


if __name__ == "__main__":
    with open(INPUT) as fp:
        content = [list(line.strip()) for line in fp.readlines()]

    max_x, max_y = len(content[0]), len(content)
    (x, y) = find_start(content)
    obstacles = find_obstacles(content)

    visited = {(x, y)}
    for pos_x, pos_y, _ in walk_map(obstacles, (x, y), max_x, max_y):
        visited.add((pos_x, pos_y))
    print("result", len(visited))

    # part 2 brute force, try every position on the initial path
    # block_for_loop = 0
    # start_state = {(x, y, 0)}
    # for new_obstacle in visited - {(x, y)}:
    #     states = start_state.copy()
    #     for pos_x, pos_y, dir_i in walk_map(
    #         obstacles | {new_obstacle}, (x, y), max_x, max_y
    #     ):
    #         state = (pos_x, pos_y, dir_i)
    #         if state in states:
    #             block_for_loop += 1
    #             break
    #         states.add(state)
    #
    # print("result 2:", block_for_loop)

    # part 2 a bit smarter, preserve the initial map walk state as we go
    block_for_loop = 0
    states = {(x, y, 0)}
    tested = obstacles.copy()
    for pos_x, pos_y, dir_i in walk_map(obstacles, (x, y), max_x, max_y):
        states.add((pos_x, pos_y, dir_i))

        new_obstacle = DIRECTION_CYCLE[dir_i]((pos_x, pos_y))

        if new_obstacle in obstacles:
            # we are right up against a known obstacle, so let's consider an obstacle
            # in the new direction instead
            new_obstacle = DIRECTION_CYCLE[(dir_i + 1) % 4]((pos_x, pos_y))

        if new_obstacle in tested or not (
            0 <= new_obstacle[0] < max_x and 0 <= new_obstacle[1] < max_y
        ):
            continue

        # start a new walk from the current position with the new obstacle in place
        # we cary over the state history of the current walk
        loop_states = states.copy()
        for loop_x, loop_y, loop_dir_i in walk_map(
            obstacles | {new_obstacle},
            (pos_x, pos_y),
            max_x,
            max_y,
            direction_i=dir_i,
        ):
            if (loop_x, loop_y, loop_dir_i) in loop_states:
                # loop detected
                block_for_loop += 1
                break
            loop_states.add((loop_x, loop_y, loop_dir_i))

        # keep track of the obstacles we tested, otherwise we will add
        # an obstacle at a point on our path we've already been, which breaks everything
        tested.add(new_obstacle)

    print("result 2:", block_for_loop)
