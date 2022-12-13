import argparse
import ast
from functools import cmp_to_key


def parse(string):
    return ast.literal_eval(string)


def read(filename):
    pairs = []
    with open(filename) as f:
        l1, l2 = f.readline().strip(), f.readline().strip()
        f.readline()
        while l1 and l2:
            pairs.append((parse(l1), parse(l2)))
            l1, l2 = f.readline().strip(), f.readline().strip()
            f.readline()
    return pairs


def compare(p1, p2):

    for a, b in zip(p1, p2):
        if type(a) == type(b) == int:
            if a == b:
                continue
            else:
                return -1 if a < b else 1
        elif type(a) == int:
            a = [a]
        elif type(b) == int:
            b = [b]
        res = compare(a, b)
        if res == 0:
            continue
        else:
            return res

    # if we came through the loop without result, then size matters
    if len(p1) < len(p2):
        return -1
    elif len(p1) == len(p2):
        return 0
    else:
        return 1


def part1(pairs):
    total = 0
    for i, p in enumerate(pairs):
        if compare(p[0], p[1]) == -1:
            total += (i + 1)
    print(total)


def part2(pairs):
    all = []
    for p in pairs:
        all.append(p[0])
        all.append(p[1])
    all.append([[2]])  # add dividers
    all.append([[6]])
    all.sort(key=cmp_to_key(compare))
    div1, div2 = 0, 0
    for i, a in enumerate(all):
        if a == [[2]]:
            div1 = i + 1
        elif a == [[6]]:
            div2 = i + 1
    print(div1 * div2)


def main(filename):
    data = read(filename)
    part1(data)
    part2(data)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', type=str, required=True,
                        help='AoC example/input txt file.')
    args = parser.parse_args()
    main(args.file)
