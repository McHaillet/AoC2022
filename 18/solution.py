import argparse
import numpy as np


def read(filename):
    coords = []
    with open(filename) as f:
        line = f.readline().strip()
        while line:
            coords.append(tuple([int(x) for x in line.split(',')]))
            line = f.readline().strip()
    return coords


def adjacency_mat(grid):
    mat = np.zeros((len(grid), len(grid)), dtype=int)
    for n, p in enumerate(grid):
        x, y, z = p
        connect = set()
        [connect.add((x + i, y, z)) for i in (-1, 1)]
        [connect.add((x, y + i, z)) for i in (-1, 1)]
        [connect.add((x, y, z + i)) for i in (-1, 1)]
        for c in connect:
            if c in grid:
                mat[n, grid.index(c)] = 1
    return mat


def adjacency_mat_diag(grid):
    mat = np.zeros((len(grid), len(grid)), dtype=int)
    for n, p in enumerate(grid):
        x, y, z = p
        connect = set()
        for i in (-1, 0, 1):
            for j in (-1, 0, 1):
                for k in (-1, 0, 1):
                    if (i, j, k) != (0, 0, 0):
                        c = (x + i, y + j, z + k)
                        if c in grid:
                            mat[n, grid.index(c)] = 1
    return mat


def bounds(coords):
    x = [p[0] for p in coords]
    y = [p[1] for p in coords]
    z = [p[2] for p in coords]
    return (min(x), max(y)), (min(y), max(y)), (min(z), max(z))


def air_pockets(points, mat):
    # search over all b?
    bx, by, bz = b
    for x in range(bx[0] + 1, bx[1] - 1):
        for y in range(by[0] + 1, by[1] - 1):
            for z in range(bz[0] + 1, bz[1] - 1):
                connect = set()
                [connect.add((x + i, y, z)) for i in (-1, 1)]
                [connect.add((x, y + i, z)) for i in (-1, 1)]
                [connect.add((x, y, z + i)) for i in (-1, 1)]


def surface_area(m):
    return 6 * m.shape[0] - m.sum()


def main(filename):
    c = read(filename)
    m = adjacency_mat(c)
    surface_outside = surface_area(m)
    print(surface_outside)
    m2 = adjacency_mat_diag(c)
    b = bounds(c)
    air_inside = air_pockets(c, m)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', type=str, required=True,
                        help='AoC example/input txt file.')
    args = parser.parse_args()
    main(args.file)
