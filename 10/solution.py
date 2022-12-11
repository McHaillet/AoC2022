import argparse


def parse(string):
    if string == 'noop':
        return [0]  # noop is same as adding 0
    else:
        addx = string.split()[1]  # its noop or addx so just take second part
        return [0, int(addx)]  # add wait operation


def read(filename):
    cycles = []
    with open(filename) as f:
        line = f.readline().strip()
        while line:
            cycles += parse(line)
            line = f.readline().strip()
    return cycles


def find_signal(stack, start, incr):
    counter = start
    x = 1 + sum(stack[0:start - 1])
    signal_strength = [x * counter]
    while counter + incr <= len(stack):
        x += sum(stack[counter - 1: counter + incr - 1])
        counter += incr
        signal_strength += [x * counter]
    return signal_strength


def draw_crt(stack, row_size):
    x = 1
    counter = 0
    row = [' ', ] * row_size
    image = [[] for _ in range(len(stack) // row_size)]
    while counter - counter % row_size + row_size <= len(stack):

        if abs(x - counter % row_size) <= 1:
            row[counter % row_size] = '#'

        x += stack[counter]
        counter += 1

        if counter > 0 and counter % row_size == 0:
            image[counter // row_size - 1] = row.copy()
            row = [' ', ] * row_size

    return image


def part_1(cycles):
    print(sum(find_signal(cycles, 20, 40)))


def part_2(data):
    screen = draw_crt(data, 40)
    for s in screen:
        print(''.join(s))


def main(filename):
    cycles = read(filename)
    part_1(cycles)
    part_2(cycles)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', type=str, required=True,
                        help='AoC example/input txt file.')
    args = parser.parse_args()
    main(args.file)
