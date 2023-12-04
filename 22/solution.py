import argparse
import time
import re


rotate = {
    'R': 1,
    'L': 3,
}
face_to_step = {
    0: (0, 1),
    1: (1, 0),
    2: (0, -1),
    3: (-1, 0)
}


def read_file(fname):
    data = []
    with open(fname, "r") as file:
        for line in file:
            strip = line.strip('\n')
            if strip != "":
                data.append(strip)
    return data


def get_map(lines):
    width = max([len(l) for l in lines])
    height = len(lines)
    board = [['x', ] * width for _ in range(height)]
    for i, l in enumerate(lines):
        board[i][:len(l)] = l.replace(' ', 'x')
    return board


def get_route(string):
    return [int(x) if x.isdigit() else x for x in re.split(r'(\d+)', string) if not x == '']


def take_steps_part_1(board, start, n_steps, step):
    width, height = len(board[0]), len(board)
    current = start
    for _ in range(n_steps):
        new = (
            (current[0] + step[0]) % height,
            (current[1] + step[1]) % width,
        )
        if board[new[0]][new[1]] == 'x':
            if step[0] == 0:  # wrap around column
                row = board[new[0]]
                search_space = ''.join(row[new[1]::step[1]] + row[:new[1]:step[1]])
                wrap = re.search(r'[.#]', search_space).start()
                new = (
                    new[0],
                    (new[1] + step[1] * wrap) % width
                )
            else:  # wrap around row
                column = [board[i][new[1]] for i in range(height)]
                search_space = ''.join(column[new[0]::step[0]] + column[:new[0]:step[0]])
                wrap = re.search(r'[.#]', search_space).start()
                new = (
                    (new[0] + step[0] * wrap) % height,
                    new[1]
                )
        if board[new[0]][new[1]] == '#':
            return current
        else:  # i.e. == '.':
            current = new
    return current


def part_1(board, instructions):
    position = (0, board[0].index('.'))
    facing = 0
    for x in instructions:
        if isinstance(x, str):
            facing = (facing + rotate[x]) % 4
        else:
            position = take_steps_part_1(board, position, x, face_to_step[facing])
    return (position[0] + 1) * 1000 + (position[1] + 1) * 4 + facing


def part_2(board, instructions):
    pass


def main(fname):
    start = time.time()
    data = read_file(fname)
    map_data, route = get_map(data[:-1]), get_route(data[-1])
    total_1 = part_1(map_data, route)
    t1 = time.time()
    print(f"Part 1: {total_1}")
    print(f"Ran in {t1-start} s")
    total_2 = part_2(map_data, route)
    print(f"Part 2: {total_2}")
    print(f"Ran in {time.time()-t1} s")
    print(f"Total ran in {time.time()-start} s")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()
    filename = args.filename
    main(filename)
