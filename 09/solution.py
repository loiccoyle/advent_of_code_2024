# https://adventofcode.com/2024/day/9
from dataclasses import dataclass
from typing import Optional, Iterator
from itertools import repeat

EMPTY = "."
INPUT = "input"
TEST_INPUT = "test_input"


@dataclass
class Node:
    id: int
    val: list[int]
    free: int
    prev: Optional["Node"] = None
    next: Optional["Node"] = None

    def __str__(self) -> str:
        prev_id = self.prev.id if self.prev else None
        next_id = self.next.id if self.next else None
        return f"Node(id={self.id}, val={self.val}, free={self.free}, prev={prev_id}, next={next_id})"


def print_linked_list(root: Optional[Node]):
    current = root
    while current:
        print(current)
        current = current.next


def parse(disk_map: str) -> Iterator[str]:
    for i, char in enumerate(disk_map):
        rep = int(char)
        if i % 2:
            yield from rep * EMPTY
        else:
            yield from repeat(str(i // 2), rep)


def compact(blocks: list[str]) -> list[int]:
    n_empty = blocks.count(EMPTY)

    left = 0
    right = len(blocks) - 1
    while left <= right:
        if blocks[left] == EMPTY and blocks[right] != EMPTY:
            blocks[left] = blocks[right]
            left += 1
            right -= 1
        if blocks[left] != EMPTY:
            left += 1
        if blocks[right] == EMPTY:
            right -= 1
    return [int(block) for block in blocks[:-n_empty]]


def parse_linked_list(disk_map: str) -> tuple[Node, Node]:
    root = None
    prev_head = None

    if len(disk_map) % 2:
        disk_map += "0"

    for i, (char, free) in enumerate(zip(disk_map[0:-1:2], disk_map[1::2])):
        rep = int(char)
        new_node = Node(id=i, val=[i] * rep, free=int(free))
        if root is None:
            root = new_node
        if prev_head is not None:
            prev_head.next = new_node
            new_node.prev = prev_head
        prev_head = new_node

    if root is None or prev_head is None:
        raise ValueError("bad linked list")

    return root, prev_head


def reorg_linked_list(root: Node, head: Node) -> Node:
    while head.prev:
        # find the "tail" which has sufficient free space
        tail = root
        while tail and tail.free < len(head.val):
            tail = tail.next
            if tail is None or tail.id == head.id:
                tail = None
                break

        if tail is None:
            # no spot to move the head
            head = head.prev
            continue

        # disconnect the head
        if head.prev:
            head.prev.next = head.next
        if head.next:
            head.next.prev = head.prev

        # add the newly freed space
        if head.prev:
            head.prev.free += len(head.val) + head.free

        # insert head after tail
        next_iter = head.prev
        head.prev = tail
        if tail.next:
            tail.next.prev = head
        head.next = tail.next
        tail.next = head

        head.free = tail.free - len(head.val)
        tail.free = 0

        head = next_iter
    return root


def checksum(root: Node) -> int:
    head = root
    out = 0
    i = 0
    while head:
        for _ in range(len(head.val)):
            out += i * head.id
            i += 1
        i += head.free
        head = head.next
    return out


if __name__ == "__main__":
    with open(INPUT) as fp:
        content = fp.read().strip()

    blocks = list(parse(content))
    compact_blocks = compact(blocks)
    out = sum(i * block for i, block in enumerate(compact_blocks))
    print("result", out)

    # part 2
    # this solution doesn't make sense, and offers no advantage over the naive bruteforce solution
    root, head = parse_linked_list(content)
    root = reorg_linked_list(root, head)
    print("result 2", checksum(root))
