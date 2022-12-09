import argparse


def parse(string):
    move, n = string.split()
    return [move, ] * int(n)


def read(filename):
    moves = []
    with open(filename) as f:
        line = f.readline().strip()
        while line:
            moves += parse(line)
            line = f.readline().strip()
    return moves


def update_head(pos, move):
    move_dict = {'R': (0, 1), 'L': (0, -1), 'U': (1, 0), 'D': (-1, 0)}
    return tuple([p + m for p, m in zip(pos, move_dict[move])])


def update_tail(pos_tail, pos_head):
    if all([(t == h or abs(t - h) <= 1) for t, h in zip(pos_tail, pos_head)]):
        return pos_tail
    else:
        return tuple([t + (h - t) // 2 if (abs(h - t)) == 2 else t + (h - t)
                      for t, h in zip(pos_tail, pos_head)])


def make_moves(moves, n_tails):
    head = (0, 0)
    tails = [(0, 0) for _ in range(n_tails)]
    tail_locations = []
    for move in moves:
        head = update_head(head, move)
        tails[0] = update_tail(tails[0], head)
        for i in range(n_tails - 1):
            tails[i + 1] = update_tail(tails[i + 1], tails[i])
        tail_locations.append(tails[n_tails - 1])
    return len(set(tail_locations))


def part_1(data):
    print(make_moves(data, n_tails=1))


def part_2(data):
    print(make_moves(data, n_tails=9))


def main(filename):
    data = read(filename)
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', type=str, required=True,
                        help='File path with protein structure, either pdb or cif.')
    args = parser.parse_args()
    main(args.file)
