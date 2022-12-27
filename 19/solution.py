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


def queue_production_options(queue, time, blueprint, current_robots, current_minerals):
    # get the robots that can be produced based on current mining robots
    queue_size_before = len(queue)
    for robot, costs in blueprint.items():
        if all([current_robots[k] > 0 for k in costs.keys()]):  # if available robots can mine the materials
            max_time_steps = 0
            for mineral, needed in costs.items():
                need_to_mine = needed - current_minerals[mineral] if needed > current_minerals[mineral] else 0
                steps, leftover = divmod(need_to_mine, current_robots[mineral])
                steps = steps + 1 if leftover > 0 else steps
                if steps > max_time_steps:
                    max_time_steps = steps
            max_time_steps += 1  # always add 1 to pass time and robot is build before mining
            if (robot == 3 and not time - max_time_steps < 1) or \
                    (robot != 3 and not time - max_time_steps < 3):
                queue.append((time - max_time_steps, max_time_steps,  # new time, time steps taken
                              current_robots.copy(), current_minerals.copy(),  # current min, current robots
                              robot))  # which one to build after
    if queue_size_before == len(queue):  # if we can no longer build in the leftover time then set to end
        queue.append((0, time, current_robots.copy(), current_minerals.copy(), None))


def max_production(blueprint, time=24):
    robots = [1, 0, 0, 0]
    minerals = [0, 0, 0, 0]
    # visited = dict()
    q = []
    queue_production_options(q, time, blueprint, robots, minerals)
    max_geodes = 0
    while q:
        time, time_steps, robots, minerals, robot_to_build = q.pop(-1)

        # visit = tuple(robots)  # does not work like this
        # if visit in visited.keys():
        #     if visited[visit] >= time:
        #         visited[visit] = time
        #     else:
        #         continue
        # else:
        #     visited[visit] = time

        minerals = [m + (r * time_steps) for m, r in zip(minerals, robots)]  # mine the mineral

        if time == 0:  # cut at time 0 or when building geode robots is no
            # longer possible/effective that should remove a lot of options
            if minerals[3] > max_geodes:
                max_geodes = minerals[3]
                # print(max_geodes)
                # print(minerals, robots)
            continue
        elif time < 0:
            print('smth went wrong')

        if robot_to_build is not None:
            robots[robot_to_build] += 1  # build the robot
            for j, c in blueprint[robot_to_build].items():
                minerals[j] -= c  # pay the costs

        queue_production_options(q, time, blueprint, robots, minerals)

    return max_geodes


def part1(factory_blueprints):
    score = 0
    for i, bp in enumerate(factory_blueprints):
        # print(bp)
        geodes = max_production(bp)
        print(f'blueprint {i + 1}, max prod = {geodes}')
        score += (i + 1) * geodes
    print(f'final score = {score}')


def part2(factory_blueprints):
    score = 1
    for i, bp in enumerate(factory_blueprints[:3]):
        # print(bp)
        geodes = max_production(bp, time=32)
        print(f'blueprint {i + 1}, max prod = {geodes}')
        score * geodes
    print(f'final score = {score}')


def main(filename):
    factory_bps = read(filename)
    part1(factory_bps)
    part2(factory_bps)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', type=str, required=True,
                        help='AoC example/input txt file.')
    args = parser.parse_args()
    main(args.file)
