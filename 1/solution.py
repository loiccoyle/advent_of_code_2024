from collections import Counter

INPUT_FILE = "input"

# https://adventofcode.com/2024/day/1
if __name__ == "__main__":
    left = []
    right = []
    with open(INPUT_FILE) as fp:
        for line in fp.readlines():
            line = line.split()
            left.append(int(line[0]))
            right.append(int(line[1]))

    left.sort()
    right.sort()

    dist = 0
    for l, r in zip(left, right):
        dist += abs(l - r)
    print("dist", dist)

    # similarity
    right_count = Counter(right)
    similarity = 0
    for num in left:
        similarity += right_count.get(num, 0) * num
    print("similarity", similarity)
