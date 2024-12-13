# https://adventofcode.com/2024/day/7

INPUT = "input"
TEST_INPUT = "test_input"


Equation = tuple[int, list[int]]


def parse_line(line: str) -> Equation:
    target, values = line.split(":")
    return int(target), [int(value) for value in values.strip().split(" ")]


def can_solve(target: int, values: list[int], acc: int) -> bool:
    if acc == target:
        return True
    if not values:
        return acc == target

    head, *tail = values
    acc_mul = acc * head
    acc_sum = acc + head
    # print(f"acc={acc} value={value} acc_mul={acc_mul} acc_sum={acc_sum}")
    return can_solve(target, tail, acc=acc_mul) or can_solve(target, tail, acc=acc_sum)


def can_solve_cat(target: int, values: list[int], acc: int) -> bool:
    if acc > target:
        return False
    if not values:
        return acc == target

    head, *tail = values
    acc_mul = acc * head
    acc_sum = acc + head
    acc_cat = int(f"{acc}{head}")
    # print(f"acc={acc} value={value} acc_mul={acc_mul} acc_sum={acc_sum} acc_cat={acc_cat}")
    return (
        can_solve_cat(target, tail, acc=acc_mul)
        or can_solve_cat(target, tail, acc=acc_sum)
        or can_solve_cat(target, tail, acc=acc_cat)
    )


if __name__ == "__main__":
    with open(INPUT) as fp:
        content = [line.strip() for line in fp.readlines()]

    equations = [parse_line(line) for line in content]
    out = 0
    for target, values in equations:
        start = values.pop(0)
        if can_solve(target, values, start):
            out += target
    print("result:", out)

    # part 2
    equations = [parse_line(line) for line in content]
    out = 0
    for target, values in equations:
        start = values.pop(0)
        if can_solve_cat(target, values, start):
            out += target
    print("result 2:", out)
