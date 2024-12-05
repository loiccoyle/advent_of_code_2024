# https://adventofcode.com/2024/day/5
from collections import defaultdict
from typing import DefaultDict


TEST_INPUT = "test_input"
INPUT = "input"


def get_update_graph(update: str) -> DefaultDict[int, set]:
    update_int = list(map(int, update.split(",")))
    graph = defaultdict(set)
    for i, prev in enumerate(update_int):
        next = update_int[i + 1 :]
        graph[prev].update(next)
    return graph


def reorder(update: list[int], update_graph: DefaultDict[int, set]) -> list[int]:
    good_order_graph = defaultdict(set)
    pages = set(update)
    for page in update:
        good_order_graph[page] = update_graph[page].intersection(pages)
    good_order_graph = [
        k
        for (k, _) in sorted(
            good_order_graph.items(), key=lambda k_v: len(k_v[1]), reverse=True
        )
    ]
    return good_order_graph


if __name__ == "__main__":
    with open(INPUT) as fp:
        content = [line.strip() for line in fp.readlines()]
    split = content.index("")

    rules = content[:split]
    updates = content[split + 1 :]

    rule_graph = defaultdict(set)
    for rule in rules:
        prev, next = map(int, rule.split("|"))
        rule_graph[prev].add(next)

    result = 0
    for update in updates:
        update_graph = get_update_graph(update)
        for k, v in update_graph.items():
            if not v.issubset(rule_graph[k]):
                break
        else:
            pages = list(update_graph.keys())
            result += pages[len(pages) // 2]
    print("result", result)

    # part 2
    result_2 = 0
    for update in updates:
        update_graph = get_update_graph(update)
        for k, v in update_graph.items():
            if not v.issubset(rule_graph[k]):
                good_graph = reorder(list(update_graph.keys()), rule_graph)
                result_2 += good_graph[len(good_graph) // 2]
                break
    print("result_2", result_2)
