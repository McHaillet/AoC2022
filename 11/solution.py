import argparse
import operator
import numpy as np
from numba import jit

ops = {'+': operator.add, '*': operator.mul}


def argmax(iterable):
    return max(enumerate(iterable), key=lambda x: x[1])[0]


def create_function(op, var):
    if var == -1:
        return lambda x: ops[op](x, x)
    else:
        return lambda x: ops[op](x, var)


@jit(nopython=True)
def get_modulo(start, op_list, val_list, mod):
    # better create loop
    assert len(op_list) == len(val_list), 'error'
    result = start % mod
    for i in range(len(op_list)):
        if val_list[i] == -1:
            result = (result * result) % mod  # this is always mult
        else:
            if op_list[i] == '+':
                result = (result + val_list[i] % mod) % mod
            else:
                result = (result * (val_list[i] % mod)) % mod
    return result


class Monkey:
    def __init__(self):
        self.items = []
        self.operate = None
        self.test = -1
        self.true_to_monkey = -1
        self.false_to_monkey = -1
        self.inspections = 0

    def parse(self, lines):
        self.items = [[int(x)] for x in lines[1].split(':')[1].split(',')]
        var1, action, var2 = lines[2].split(':')[1].split()[2:5]
        self.operate = [action, -1 if var2 == 'old' else int(var2)]
        self.test = int(lines[3].split(':')[1].split()[2])
        self.true_to_monkey = int(lines[4].split(':')[1].split()[3])
        self.false_to_monkey = int(lines[5].split(':')[1].split()[3])


class MonkeyBusiness:
    def __init__(self, monkey_list):
        self._list = monkey_list

    def run_round(self, with_relief=True):
        for monkey in self._list:
            for _ in range(len(monkey.items)):
                item = monkey.items.pop(0)
                monkey.inspections += 1
                if with_relief:
                    nitem = int(create_function(*monkey.operate)(item[0]) / 3)
                    if nitem % monkey.test == 0:
                        self._list[monkey.true_to_monkey].items.append([nitem])
                    else:
                        self._list[monkey.false_to_monkey].items.append([nitem])
                else:
                    item.append(monkey.operate)  # should be able to pre-sum the addition operations
                    # calculate modulo and throw
                    if get_modulo(item[0], np.array([a[0] for a in item[1:]], dtype=str),
                                  np.array([a[1] for a in item[1:]], dtype=int), monkey.test) == 0:
                        self._list[monkey.true_to_monkey].items.append(item)
                    else:
                        self._list[monkey.false_to_monkey].items.append(item)

    def finalise(self, n=2):
        inspecs = [m.inspections for m in self._list]
        score = 1
        for _ in range(n):
            i = argmax(inspecs)
            score *= inspecs.pop(i)
        return score

    def print_state(self):
        print([m.inspections for m in self._list])

    def find_mod(self):  # should have used this!
        print(np.lcm.reduce([m.test for m in self._list]))


def read(filename):
    with open(filename) as f:
        data = f.readlines()

    monkeys = []
    for i in range(0, len(data), 7):
        monkeys.append(Monkey())
        monkeys[-1].parse(data[i:i+6])
    return MonkeyBusiness(monkeys)


def part_1(monkeys):
    for _ in range(20):
        monkeys.run_round(with_relief=True)
    print(monkeys.finalise())


def part_2(monkeys):
    monkeys.find_mod()
    for i in range(1000):
        if i % 1000 == 0:
            monkeys.print_state()
        monkeys.run_round(with_relief=False)
    monkeys.print_state()
    print(monkeys.finalise())


def main(filename):
    monkeys = read(filename)
    part_1(monkeys)
    monkeys = read(filename)  # reread to reset the monkeys
    part_2(monkeys)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', type=str, required=True,
                        help='AoC example/input txt file.')
    args = parser.parse_args()
    main(args.file)
