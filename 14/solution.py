import argparse
import numpy as np
import time


def parse(string):
    c = []
    x = string.split()
    for i in range(0, len(x), 2):
        c.append(eval(x[i]))
    return c


def read(filename):
    d = []
    with open(filename) as f:
        line = f.readline().strip()
        while line:
            d.append(parse(line))
            line = f.readline().strip()
    return d


def find_bounds(x):
    y_min, y_max = 0, 0
    x_min, x_max = 500, 500
    for l in x:
        for c in l:
            if c[1] > y_max:
                y_max = c[1]
            if c[0] < x_min:
                x_min = c[0]
            if c[0] > x_max:
                x_max = c[0]
    return x_min, x_max, y_min, y_max


def place_sand(cave, x, xmax, ymax):
    for y in range(ymax - 1):
        if cave[x, y + 1] > 0:
            if x - 1 >= 0 and cave[x - 1, y + 1] > 0:
                if x + 1 < xmax and cave[x + 1, y + 1] > 0:
                    cave[x, y] = 2
                    return True
                else:
                    x += 1
            else:
                x -= 1
    return False


def part1(inp):
    xl, xu, yl, yu = find_bounds(inp)
    cave = np.zeros((xu - xl + 1, yu - yl + 1))
    for rock in inp:
        for c1, c2 in zip(rock[0:-1], rock[1:]):
            xrange = (c1[0] - xl, c2[0] - xl) if c1[0] < c2[0] else (c2[0] - xl, c1[0] - xl)
            yrange = (c1[1], c2[1]) if c1[1] < c2[1] else (c2[1], c1[1])
            cave[xrange[0]: xrange[1] + 1, yrange[0]:yrange[1] + 1] = 1  # 1 == rock
    count = 0
    while place_sand(cave, 500 - xl, xu + 1, yu + 1):
        count += 1
    print(count)


def part2(inp):
    xl, xu, yl, yu = find_bounds(inp)
    yu += 2  # increase for bottom row
    xl, xu = 500 - yu, 500 + yu
    cave = np.zeros((xu - xl + 1, yu - yl + 1))
    cave[:, -1] = 1
    for rock in inp:
        for c1, c2 in zip(rock[0:-1], rock[1:]):
            xrange = (c1[0] - xl, c2[0] - xl) if c1[0] < c2[0] else (c2[0] - xl, c1[0] - xl)
            yrange = (c1[1], c2[1]) if c1[1] < c2[1] else (c2[1], c1[1])
            cave[xrange[0]: xrange[1] + 1, yrange[0]:yrange[1] + 1] = 1  # 1 == rock
    # append cave
    count = 0
    while place_sand(cave, 500 - xl, xu + 1, yu + 1):
        count += 1
        if cave[500 - xl, 0] == 2:
            break
    print(count)


def main(filename):
    s = time.time()
    data = read(filename)
    part1(data)
    part2(data)
    print(time.time() - s)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', type=str, required=True,
                        help='AoC example/input txt file.')
    args = parser.parse_args()
    main(args.file)
