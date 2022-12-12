import argparse


def read(filename):
    data = []
    with open(filename) as f:
        line = f.readline().strip()
        while line:
            data.append([ord(a) for a in line])
            line = f.readline().strip()
    return data


def find_start_end(m):
    start, end = (-1, -1), (-1, -1)
    for i, row in enumerate(m):
        for j, col in enumerate(row):
            if col == 83:
                m[i][j] = ord('a')
                start = (i, j)
            if col == 69:
                m[i][j] = ord('z')
                end = (i, j)
    return start, end


def find_all_starts(m):
    starts = []
    for i, row in enumerate(m):
        for j, col in enumerate(row):
            if m[i][j] == ord('a'):
                starts.append((i, j))
    return starts


def get_moves(m, loc, previous_locs):
    if loc[0] == 0:
        x = [(1, loc[1])]
    elif loc[0] == len(m) - 1:
        x = [(len(m) - 2, loc[1])]
    else:
        x = [(loc[0] - 1, loc[1]), (loc[0] + 1, loc[1])]

    if loc[1] == 0:
        y = [(loc[0], 1)]
    elif loc[1] == len(m[0]) - 1:
        y = [(loc[0], len(m[0]) - 2)]
    else:
        y = [(loc[0], loc[1] - 1), (loc[0], loc[1] + 1)]

    return [o for o in x + y if
            (m[o[0]][o[1]] - m[loc[0]][loc[1]] < 2 and o not in previous_locs)]  # not last location


def find_routes(mounts, s, e):
    visited = set()
    steps = 0
    if isinstance(s, list):
        stack = [(a, steps) for a in s]
    else:
        stack = [(s, steps)]
    while stack:
        current, steps = stack.pop(0)

        # get move options
        options = [(m, steps + 1) for m in get_moves(mounts, current, visited)]

        # return if we found the end
        if any([o[0] == e for o in options]):
            return steps + 1

        # add stack and visisted
        stack += options
        [visited.add(o[0]) for o in options]


def part_1(mountains, start, end):
    print(find_routes(mountains, start, end))


def part_2(mountains, start, end):
    starts = find_all_starts(mountains)
    print(find_routes(mountains, starts, end))


def main(filename):
    m = read(filename)
    s, e = find_start_end(m)
    part_1(m, s, e)
    part_2(m, s, e)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', type=str, required=True,
                        help='AoC example/input txt file.')
    args = parser.parse_args()
    main(args.file)
