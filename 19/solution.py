import argparse
import heapq
from tqdm import tqdm

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


def queue_production_options(queue, time, blueprint, current_robots, current_minerals, score):
    queue_size_before = len(queue)  # record queue size before adding new options
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
            if robot == 3 and not time - max_time_steps < 1:
                heapq.heappush(queue, (score - (time - max_time_steps),
                                       (time - max_time_steps, max_time_steps,  # new time, time steps taken
                                        current_robots.copy(), current_minerals.copy(),  # current min, current robots
                                        robot)))
            elif robot != 3 and not time - max_time_steps < 2:
                heapq.heappush(queue, (score,
                                       (time - max_time_steps, max_time_steps,  # new time, time steps taken
                                        current_robots.copy(), current_minerals.copy(),  # current min, current robots
                                        robot)))  # which one to build after
    if queue_size_before == len(queue):  # if we can no longer build in the leftover time then set to end
        heapq.heappush(queue, (score, (0, time, current_robots.copy(), current_minerals.copy(), None)))


def max_production(blueprint, time=24):
    robots = [1, 0, 0, 0]
    minerals = [0, 0, 0, 0]
    score = 0
    visited = {t: score for t in range(time - 1, -1, -1)}
    q = []
    heapq.heapify(q)
    queue_production_options(q, time, blueprint, robots, minerals, score)
    max_geodes = 0
    while q:
        score, (time, time_steps, robots, minerals, robot_to_build) = heapq.heappop(q)

        # check if this is the optimal path so far
        if score < visited[time]:
            [visited.update({t: score}) for t in range(time, -1, -1) if score < visited[t]]
        elif score > visited[time]:
            continue

        minerals = [m + (r * time_steps) for m, r in zip(minerals, robots)]  # mine the mineral

        if time == 0:  # cut at time 0 or when building geode robots is no
            # longer possible/effective that should remove a lot of options
            if abs(score) > max_geodes:
                max_geodes = abs(score)
            continue

        if robot_to_build is not None:
            robots[robot_to_build] += 1  # build the robot
            for j, c in blueprint[robot_to_build].items():
                minerals[j] -= c  # pay the costs

        queue_production_options(q, time, blueprint, robots, minerals, score)

    return max_geodes


def part1(factory_blueprints):
    score = 0
    for i in tqdm(range(len(factory_blueprints))):
        geodes = max_production(factory_blueprints[i])
        score += (i + 1) * geodes
    print(f'part 1 = {score}')


def part2(factory_blueprints):
    score = 1
    for i in tqdm(range(3)):
        geodes = max_production(factory_blueprints[i], time=32)
        score *= geodes
    print(f'part 2 = {score}')


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
