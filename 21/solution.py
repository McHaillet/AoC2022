import argparse
import time
from operator import add, sub, mul, truediv


op_map = {
    '+': add,
    '-': sub,
    '*': mul,
    '/': truediv,
}
op_invert = {
    '+': sub,
    '-': add,
    '*': truediv,
    '/': mul,
}


def read_file(fname):
    data = dict()
    with open(fname, "r") as file:
        for line in file:
            strip = line.strip()
            if strip != "":
                data[strip.split(':')[0]] = strip.replace(':', '=')
    return data


def parse(string):
    equation = {}
    equation['y'], func = string.split('=')
    operator = None
    for op in op_map.keys():
        if op in func:
            operator = op
    if operator is None:
        equation['op'] = None
        equation['xs'] = func.strip()
    else:
        equation['op'] = operator
        equation['xs'] = [x.strip() for x in func.split(operator)]
    return equation


def solve_down(data, start_from='root', break_on=None):
    if start_from == break_on:
        raise ValueError
    equation = parse(data[start_from])
    if equation['op'] is None:
        return float(equation['xs'])
    else:
        return op_map[equation['op']](
            solve_down(data, start_from=equation['xs'][0], break_on=break_on),
            solve_down(data, start_from=equation['xs'][1], break_on=break_on)
        )


def solve_up(data, start_from='humn', final='root', result=0):
    if start_from == final:
        return result
    # there can only be one equation that contains starts_from as a variable
    equation = parse([x for x in data.values() if start_from in x and not x.startswith(start_from)][0])
    # get the value of the other variable in this equation
    value = solve_down(data, start_from=[v for v in equation['xs'] if v != start_from][0])
    if equation['op'] == '-' and equation['xs'].index(start_from) == 1:
        f = lambda x: -1 * x
    elif equation['op'] == '/' and equation['xs'].index(start_from) == 1:
        f = lambda x: 1 / x
    else:
        f = lambda x: x
    return op_invert[equation['op']](
        f(solve_up(data, start_from=equation['y'], final=final, result=result)),
        value
    )


def part_1(data):
    return int(solve_down(data, start_from='root'))


def part_2(data):
    vars = parse(data['root'])['xs']

    try:
        known, solve = vars
        result = solve_down(data, start_from=known, break_on='humn')
    except ValueError:
        known, solve = vars[1], vars[0]
        result = solve_down(data, start_from=known, break_on='humn')

    # print('solve =', solve)
    # print('result =', result)

    solution = solve_up(data, start_from='humn', final=solve, result=result)
    return int(solution)


def main(fname):
    start = time.time()
    data = read_file(fname)
    total_1 = part_1(data)
    t1 = time.time()
    print(f"Part 1: {total_1}")
    print(f"Ran in {t1-start} s")
    total_2 = part_2(data)
    print(f"Part 2: {total_2}")
    print(f"Ran in {time.time()-t1} s")
    print(f"Total ran in {time.time()-start} s")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()
    filename = args.filename
    main(filename)
