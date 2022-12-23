import argparse

ore_to_id = {'ore': 0,
             'clay': 1,
             'obsidian': 2,
             'geodes': 3}


def parse(bp):
    robots = {}
    bp = bp.split(':')[1].split('.')
    for i, l in enumerate(bp[:-1]):
        words = l.split()
        robot = {}
        for cost, mineral in zip(words[4: -1], words[5:]):
            if cost not in ore_to_id.keys() and cost != 'and':
                robot[ore_to_id[mineral]] = int(cost)
        robots[i] = robot
    return robots


def read(filename):
    factories = []
    with open(filename) as f:
        line = f.readline().strip()
        while line:
            factories.append(parse(line))
            line = f.readline().strip()
    return factories


def production_options(blueprint, minerals):
    options = [False, ] * 4
    for robot, costs in blueprint.items():
        options[robot] = all([v <= minerals[k] for k, v in costs.items()])
    return options


def max_production(blueprint):
    robots = [1, 0, 0, 0]
    minerals = [0, 0, 0, 0]
    time = 24
    q = [(time, robots, minerals)]
    max_geodes = 0
    while q:
        time, robots, minerals = q.pop()
        if time == 0:
            if minerals[3] > max_geodes:
                max_geodes = minerals[3]
                print(max_geodes)
            continue
        minerals = [m + r for m, r in zip(minerals, robots)]
        choices = production_options(blueprint, minerals)
        # append choices to q
        for i, choice in enumerate(choices):
            if choice:  # could reduce time by removing irrelevant choices
                # if you buy a clay robot next and you have enough ore it does not make sense to wait longer
                r, m = robots.copy(), minerals.copy()
                r[i] += 1
                for j, c in blueprint[i].items():
                    m[j] -= c
                q.append((time - 1, r, m))
        q.append((time - 1, robots, minerals))  # just wait
    return max_geodes


def main(filename):
    factory_bps = read(filename)
    print(factory_bps)
    for bp in factory_bps:
        print(max_production(bp))
    # print(data)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', type=str, required=True,
                        help='AoC example/input txt file.')
    args = parser.parse_args()
    main(args.file)
