# https://adventofcode.com/2024/day/2
INPUT_FILE = "input"


# check if a report (row) is "safe"
def is_safe(report: list[int]) -> bool:
    # the expected sign of the report, either -1 or 1
    sign = None
    for prev, next in zip(report[:-1], report[1:]):
        diff = next - prev
        abs_diff = abs(diff)
        if 3 < abs_diff or abs_diff == 0:
            # if the abs diff is too big abort early
            return False
        # get the sign of the diff
        diff_sign = diff // abs_diff
        if sign is None:
            # set the expected sign for the rest of the report
            sign = diff_sign
        if diff_sign != sign:
            # if the signs don't match abort
            return False
    return True


if __name__ == "__main__":
    with open(INPUT_FILE) as fp:
        input = [list(map(int, line.split())) for line in fp.readlines()]

    n_safe = 0
    for report in input:
        if is_safe(report):
            n_safe += 1
    print("n safe", n_safe)

    # part 2
    n_safe = 0
    for report in input:
        if is_safe(report):
            n_safe += 1
        else:
            # brute force, drop element by element and test
            for i in range(len(report)):
                # drop an element and test
                popped = report.pop(i)
                if is_safe(report):
                    n_safe += 1
                    break
                # add the element back in the list
                report.insert(i, popped)
    print("n safe with 1 removal", n_safe)
