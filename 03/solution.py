# https://adventofcode.com/2024/day/3
import re

INPUT = "input"


PATTERN = re.compile(r"mul\((\d+),(\d+)\)")


def compute(input: str) -> int:
    return sum([int(match[0]) * int(match[1]) for match in re.findall(PATTERN, input)])


if __name__ == "__main__":
    with open(INPUT) as fp:
        content = fp.read()
    print("result", compute(content))

    # part 2
    disabled = re.compile(r"don't\(\)(.*?)(do\(\)|$)", re.DOTALL)
    # remove the disabled parts
    content = re.sub(disabled, "", content)
    # same as above
    print("part 2 result", compute(content))
