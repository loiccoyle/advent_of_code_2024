from collections import deque, Counter


INPUT = "input"
TEST_INPUT = "test_input"
N_BLINKS = 25


def blink(stones: deque[int]) -> deque[int]:
    for _ in range(len(stones)):
        value = stones.popleft()
        if value == 0:
            stones.append(1)
        else:
            digits = str(value)
            n = len(digits)
            if n % 2 == 0:
                half = n // 2
                left = int(digits[:half])
                right = int(digits[half:])
                stones.extend([left, right])
            else:
                stones.append(value * 2024)
    return stones


def blink_counter(stones: Counter[int]) -> Counter[int]:
    next_stones = Counter()

    for value, count in stones.items():
        if value == 0:
            next_stones[1] += count
        else:
            digits = str(value)
            n = len(digits)
            if n % 2 == 0:
                half = n // 2
                left = int(digits[:half])
                right = int(digits[half:])
                next_stones[left] += count
                next_stones[right] += count
            else:
                next_stones[value * 2024] += count

    return next_stones


if __name__ == "__main__":
    with open(INPUT) as fp:
        content = fp.readline().strip()

    values = [int(v) for v in content.split()]
    stones = deque(values)

    for _ in range(N_BLINKS):
        stones = blink(stones)
    print("result", len(stones))

    # part 2
    stones = Counter(values)
    for _ in range(75):
        stones = blink_counter(stones)
    print("result 2", sum(stones.values()))
