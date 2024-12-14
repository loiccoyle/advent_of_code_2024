import re
from pathlib import Path

import numpy as np
from PIL import Image

INPUT = "input"
INPUT_DIM = (101, 103)
TEST_INPUT = "test_input"
TEST_DIM = (11, 7)


def parse_input(content_raw: str):
    pattern = re.compile(r"p=(\d*),(\d*) v=(-?\d*),(-?\d*)")
    pos_vel = np.array(
        [tuple(map(int, match)) for match in re.findall(pattern, content_raw)]
    )
    pos = pos_vel[:, :2]
    vel = pos_vel[:, 2:]
    return pos, vel


def simulate(pos, vel, steps: int = 100, dimensions: tuple[int, int] = INPUT_DIM):
    result = pos + vel * steps
    # return result
    return np.mod(result, dimensions)


def quadrant_count(pos, dimensions: tuple[int, int] = INPUT_DIM):
    v_line = dimensions[0] // 2
    h_line = dimensions[1] // 2
    top_left = ((pos[:, 0] < v_line) & (pos[:, 1] < h_line)).sum()
    top_right = ((pos[:, 0] > v_line) & (pos[:, 1] < h_line)).sum()
    bottom_left = ((pos[:, 0] < v_line) & (pos[:, 1] > h_line)).sum()
    bottom_right = ((pos[:, 0] > v_line) & (pos[:, 1] > h_line)).sum()
    print(top_left, top_right, bottom_left, bottom_right)
    return top_left * top_right * bottom_left * bottom_right


if __name__ == "__main__":
    with open(INPUT) as fp:
        content_raw = fp.read()
    pos, vel = parse_input(content_raw)
    state = simulate(pos, vel, steps=100)
    print("result", quadrant_count(state))

    # part 2
    img_dir = Path("imgs")
    img_dir.mkdir(exist_ok=True)
    min_variance = np.inf
    for step in range(10000):
        state = simulate(pos, vel, steps=step)
        variance = np.var(state)
        if variance < min_variance:
            min_variance = variance
            board = np.zeros(INPUT_DIM[::-1])
            board[state[:, 1], state[:, 0]] = 255
            img = Image.fromarray(board).convert("RGB")
            img.save(img_dir / f"frame_{step}.jpg")
