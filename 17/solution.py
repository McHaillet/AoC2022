import argparse
import numpy as np
import time

shapes = {0: np.ones((1, 4), dtype=bool),
          1: np.array([[0, 1, 0],
                       [1, 1, 1],
                       [0, 1, 0]], dtype=bool),
          2: np.array([[1, 1, 1],
                       [0, 0, 1],
                       [0, 0, 1]], dtype=bool),
          3: np.ones((4, 1), dtype=bool),
          4: np.ones((2, 2), dtype=bool)}
combined_height = 13


def valid(cavern, rock, row, col):
    place = cavern[row: row + rock.shape[0], col: col + rock.shape[1]]
    return not np.any(np.logical_and(place, rock))


class Cave:
    def __init__(self, airflow):
        self._flow = airflow
        self._n_ops = len(self._flow)
        self._air_index = 0
        # max height of chamber for the number of rocks
        # pre initialize to save time?
        self._cavern = np.zeros((1_000_000, 7), dtype=bool)
        self._top_height = 0
        self._bottom_height = 0

    def drop_rock(self, rock):
        height = self._top_height + 3
        col = 2
        while True:
            # do air flow
            f = self._flow[self._air_index % self._n_ops]
            if f == '<' and col > 0 and valid(self._cavern, rock, height, col - 1):
                col -= 1
            elif f == '>' and col + rock.shape[1] < 7 and valid(self._cavern, rock, height, col + 1):
                col += 1
            self._air_index += 1  # always update air index
            # do drop
            if not height == 0 and valid(self._cavern, rock, height - 1, col):
                height -= 1
            else:
                self._cavern[height: height + rock.shape[0], col: col + rock.shape[1]] += rock
                self._top_height = height + rock.shape[0] \
                    if height + rock.shape[0] > self._top_height else self._top_height
                break

    def run(self):
        cache = dict()
        n_rocks = 1_000000_000000
        for i in range(n_rocks):
            if i == 2022:
                print(self._top_height)
            key = i % 5, self._air_index % self._n_ops
            if key in cache:
                step, top = cache[key]
                d, m = divmod(n_rocks - i, i - step)
                if m == 0:
                    print(self._top_height + (self._top_height - top) * d)
                    break
            else:
                cache[key] = i, self._top_height
            self.drop_rock(shapes[i % 5])


def read(filename):
    with open(filename) as f:
        line = f.readline().strip()
    return line


def main(filename):
    s = time.time()
    flow = read(filename)
    c = Cave(flow)
    c.run()
    print(time.time() - s)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', type=str, required=True,
                        help='AoC example/input txt file.')
    args = parser.parse_args()
    main(args.file)
