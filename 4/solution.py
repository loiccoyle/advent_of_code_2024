# https://adventofcode.com/2024/day/4
from typing import Iterable


INPUT = "input"
TEST_INPUT = """MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX""".split()


def rotate_90(content: list[str]) -> list[str]:
    transposed = list(map("".join, zip(*content)))
    rotated = [row[::-1] for row in transposed]
    return rotated


def find_left_right(content: list[str]) -> int:
    out = 0
    for row in content:
        out += row.count("XMAS")
    return out


def content_diags(content: list[str]) -> list[str]:
    diags = [[] for _ in range(len(content) * 2 - 1)]
    for x in range(len(content)):
        for y in range(len(content)):
            diags[x + y].append(content[y][x])
    return ["".join(diag) for diag in diags]


def rolling_window(content: list[str], window_width: int = 3) -> Iterable[list[str]]:
    for i in range(len(content)):
        if i + window_width > len(content):
            continue
        rows = content[i : i + window_width]
        for j in range(len(content)):
            if j + window_width > len(content):
                continue
            window = [rows[k][j : j + window_width] for k in range(len(rows))]
            yield window


if __name__ == "__main__":
    with open(INPUT) as fp:
        content = [line.strip() for line in fp.readlines()]

    result = 0
    # rotate 4 times, at each rotation check the rows and the bottom left to top right diags
    for _ in range(4):
        result += find_left_right(content)
        result += find_left_right(content_diags(content))
        content = rotate_90(content)
    print("result", result)

    # part 2
    result_2 = 0
    valid_cross = {"MS", "SM"}
    # rolling window over the text and check the cross pattern
    for window in rolling_window(content):
        if window[1][1] != "A":
            continue
        if (window[0][0] + window[2][2] not in valid_cross) or (
            window[2][0] + window[0][2] not in valid_cross
        ):
            continue
        result_2 += 1
    print("result_2", result_2)
