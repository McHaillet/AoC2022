import argparse
from tqdm import tqdm  # progress bar


def read(filename):
    data = []
    with open(filename) as f:
        line = f.readline().strip()
        while line:
            data.append(int(line))
            line = f.readline().strip()
    return data


def decrypt(encrypted_data, times=1):
    locations = [i for i, _ in enumerate(encrypted_data)]  # can store here where number move to
    n_elements = len(encrypted_data)
    for x in tqdm(range(n_elements * times)):
        i = x % n_elements
        current_loc = locations.index(i)
        new_loc = (current_loc + encrypted_data[i]) % (n_elements - 1) or n_elements
        locations[current_loc: current_loc + 1] = []
        locations[new_loc: new_loc] = [i]
    return [encrypted_data[i] for i in locations]


def part1(inp):
    decrypted = decrypt(inp)
    if len(decrypted) < 10: print(decrypted)
    start = decrypted.index(0)
    sum = 0
    for s in [1, 2, 3]:
        sum += decrypted[(start + s * 1000) % len(decrypted)]
    print(sum)


def part2(inp):
    decrypted = decrypt([n * 811589153 for n in inp], times=10)
    start = decrypted.index(0)
    sum = 0
    for s in [1, 2, 3]:
        sum += decrypted[(start + s * 1000) % len(decrypted)]
    print(sum)


def main(filename):
    inp = read(filename)
    part1(inp)
    part2(inp)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', type=str, required=True,
                        help='AoC example/input txt file.')
    args = parser.parse_args()
    main(args.file)