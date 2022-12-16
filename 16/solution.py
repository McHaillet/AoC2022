import argparse
import time
from queue import PriorityQueue


def read(filename):
    rates, network = {}, {}
    with open(filename) as f:
        line = f.readline().strip()
        while line:
            r, n = line.split(';')
            # split valve
            parts = r.split()
            rates[parts[1]] = int(parts[4].split('=')[1])
            # split connections
            network[parts[1]] = [s.strip(',') for s in n.split()[4:]]
            line = f.readline().strip()
    return rates, network


def find_shortest(start, dest, connections, visited, steps):
    steps += 1
    visited.append(start)
    paths = []
    for c in connections[start]:
        if c in visited:
            continue
        elif c == dest:
            return steps
        else:
            res = find_shortest(c, dest, connections, visited.copy(), steps)
            if type(res) == int:
                paths.append(res)
    return min(paths) if len(paths) > 0 else []


class Graph:
    def __init__(self, flow_rates, connections, start='AA'):
        self.vertices = list(flow_rates.keys())
        self.weights = {t: -r for t, r in flow_rates.items() if r > 0}
        self.valves = set(self.weights.keys())
        self.network = {v: {n: 0 for n in self.weights.keys()} for v in self.weights.keys()}
        self.start = {v: 0 for v in self.weights.keys()}
        # count distances
        for v in self.network.keys():
            for n in self.network[v].keys():
                if v != n:
                    # find shortest?
                    self.network[v][n] = find_shortest(v, n, connections, [], 1)  # add one for opening valve
            self.start[v] = find_shortest(start, v, connections, [], 1)

    def dijkstra(self, minutes=30):
        dist = {}

        q = []
        # distance, minutes, opened valves, visited, current
        for s, t in self.start.items():
            q.append((self.weights[s] * (minutes - t), minutes - t, set([s]), s))

        shortest = 0

        while q:
            # keep track of a visited set and reset upon valve opening
            (d, minutes, opened, current_vertex) = q.pop()

            openable = self.valves - opened
            if len(openable) == 0 or all([self.network[current_vertex][o] > minutes for o in openable]):
                if d < shortest:
                    shortest = d
                continue

            for n in openable:
                time_step = self.network[current_vertex][n]
                if time_step > minutes:
                    continue
                np = opened.copy()
                np.add(n)
                new_cost = d + self.weights[n] * (minutes - time_step)
                if ''.join(np) not in dist.keys():
                    dist[''.join(np)] = new_cost
                    q.append((new_cost, minutes - time_step, np, n))
                else:
                    if new_cost < dist[''.join(np)]:
                        dist[''.join(np)] = new_cost
                        q.append((new_cost, minutes - time_step, np, n))
        return shortest

    def dijkstra2(self, minutes=26):
        dist = {}

        q = []
        # distance, minutes, opened valves, visited, current
        for s, t in self.start.items():
            for s2, t2 in self.start.items():
                if s != s2:
                    q.append((self.weights[s] * (minutes - t) + self.weights[s2] * (minutes - t2),
                              minutes - t, minutes - t2, s, s2, set([s, s2])))

        shortest = 0

        while q:
            # keep track of a visited set and reset upon valve opening
            (d, m1, m2, loc1, loc2, opened) = q.pop()

            openable = self.valves - opened
            if len(openable) == 0 or (all([self.network[loc1][o] > m1 for o in openable]) and
                                      all([self.network[loc2][o] > m2 for o in openable])):
                if d < shortest:
                    shortest = d
                continue

            for n in openable:
                time_step = self.network[loc1][n]
                if time_step > m1:
                    continue
                np = opened.copy()
                np.add(n)
                new_cost = d + self.weights[n] * (m1 - time_step)
                if ''.join(np) not in dist.keys():
                    dist[''.join(np)] = new_cost
                    q.append((new_cost, m1 - time_step, m2, n, loc2, np))
                else:
                    if new_cost < dist[''.join(np)]:
                        dist[''.join(np)] = new_cost
                        q.append((new_cost, m1 - time_step, m2, n, loc2, np))
            for n in openable:
                time_step = self.network[loc2][n]
                if time_step > m2:
                    continue
                np = opened.copy()
                np.add(n)
                new_cost = d + self.weights[n] * (m2 - time_step)
                if ''.join(np) not in dist.keys():
                    dist[''.join(np)] = new_cost
                    q.append((new_cost, m1, m2 - time_step, loc1, n, np))
                else:
                    if new_cost < dist[''.join(np)]:
                        dist[''.join(np)] = new_cost
                        q.append((new_cost, m1, m2 - time_step, loc1, n, np))
        return shortest


def main(filename):
    s = time.time()
    valves = Graph(*read(filename))
    print(-valves.dijkstra())
    print(-valves.dijkstra2())
    print(time.time() - s)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', type=str, required=True,
                        help='AoC example/input txt file.')
    args = parser.parse_args()
    main(args.file)
