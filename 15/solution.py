import argparse
import time


def parse(string):
    sensor, beacon = [s.strip(',') for s in string.split(':')]
    sensor = tuple([int(s.split('=')[1].strip(',')) for s in sensor.split()[2:4]])
    beacon = tuple([int(s.split('=')[1].strip(',')) for s in beacon.split()[4:6]])
    return sensor, beacon


def read(filename):
    d = []
    with open(filename) as f:
        line = f.readline().strip()
        while line:
            d.append(parse(line))
            line = f.readline().strip()
    return d


def manhattan(c1, c2):
    return abs(c1[0] - c2[0]) + abs(c1[1] - c2[1])


def find_section(ranges):
    ranges.sort()
    section = list(ranges[0])
    for r in ranges[1:]:
        if r[0] <= section[-1]:
            section[-1] = r[1] if section[-1] < r[1] else section[-1]
        else:
            section += r
    return section


def find_section2(ranges):
    ranges.sort()
    section = list(ranges[0])
    flag = False
    for r in ranges[1:]:
        if r[0] <= section[-1]:
            section[-1] = r[1] if section[-1] < r[1] else section[-1]
        else:
            section += r
            flag = True
    return flag, section


def covered(section, beacons):
    count = 0
    for b in beacons:
        if len(section) == 4:
            if section[2] <= b <= section[3]:
                count += 1
        if section[0] <= b <= section[1]:
            count += 1
    size = 0 - count
    if len(section) == 4:
        size += section[3] - section[2] + 1
    size += section[1] - section[0] + 1
    return size


def part1(inp, row):
    ranges = []
    beacons_on_row = set()
    for d in inp:
        s, b = d
        if b[1] == row:
            beacons_on_row = beacons_on_row.union([b[0]])
        dist = manhattan(s, b)
        ydiff = dist - abs(s[1] - row)
        if ydiff > 0:
            x1 = s[0] - ydiff
            x2 = s[0] + ydiff
            ranges.append((x1, x2))
    section = find_section(ranges)
    print(covered(section, beacons_on_row))


def part2(inp, limit):
    rmin, rmax = limit
    for row in range(rmax):
        ranges = []
        for d in inp:
            s, b = d
            dist = manhattan(s, b)
            ydiff = dist - abs(s[1] - row)
            if ydiff > 0:
                x1 = s[0] - ydiff
                x2 = s[0] + ydiff
                x1 = 0 if x1 < rmin else (rmax if x1 > rmax else x1)
                x2 = 0 if x2 < rmin else (rmax if x2 > rmax else x2)
                ranges.append((x1, x2 + 1))
        flag, section = find_section2(ranges)
        if flag:
            print(section[1] * 4000000 + row)
            break


def main(filename):
    s = time.time()
    data = read(filename)
    part1(data, 2_000_000)
    part2(data, (0, 4_000_001))
    print(time.time() - s)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', type=str, required=True,
                        help='AoC example/input txt file.')
    args = parser.parse_args()
    main(args.file)
