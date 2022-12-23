import argparse
import numpy as np

moves = [(-1, 0, 0), (1, 0, 0), (0, -1, 0), (0, 1, 0), (0, 0, -1), (0, 0, 1)]


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


def surface_area(m):
    return 6 * m.shape[0] - m.sum()


def bounds(coords):
    x = [p[0] for p in coords]
    y = [p[1] for p in coords]
    z = [p[2] for p in coords]
    return (min(x), max(y) + 1), (min(y), max(y) + 1), (min(z), max(z) + 1)


def air_pockets(points, bounds):
    # search over all b?
    bx, by, bz = bounds
    xx, yy, zz = list(range(*bx)), list(range(*by)), list(range(*bz))
    grid = set()
    for x in xx:
        for y in yy:
            for z in zz:
                if not (x, y, z) in points:
                    grid.add((x, y, z))
    # excluded = []
    pockets = []
    while grid:  # find all connected components
        air_can_evaporate = False
        visited = set()
        q = [grid.pop()]
        while q:
            p = q.pop()
            visited.add(p)
            if p in grid:
                grid.remove(p)
            for m in moves:
                x, y, z = [a + i for a, i in zip(p, m)]
                if (x, y, z) in visited or (x, y, z) in points:
                    continue
                elif x <= bx[0] or x >= bx[1]\
                        or y <= by[0] or y >= by[1]\
                        or z <= bz[0] or z >= bz[1]:
                    air_can_evaporate = True
                else:
                    q.append((x, y, z))
        if not air_can_evaporate:
            pockets += list(visited)
        # else: excluded += list(visited)
    return pockets


def main(filename):
    c = read(filename)
    m = adjacency_mat(c)
    surface_outside = surface_area(m)
    print(surface_outside)
    air_inside = air_pockets(set(c), bounds(c))
    m2 = adjacency_mat(air_inside)
    surface_inside = surface_area(m2)
    print(surface_outside - surface_inside)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', type=str, required=True,
                        help='AoC example/input txt file.')
    args = parser.parse_args()
    main(args.file)
