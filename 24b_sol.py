import argparse
from math import trunc


def main():
    constraints = [9 for _ in range(14)]
    y = []
    digit = -1
    const = False
    with open(args.f, "r") as f:
        for row in f:
            if row.startswith("div z"):
                if row.strip().split()[-1] != "1":
                    const = True
                else:
                    const = False
                digit += 1
                row = next(f)
                x = int(row.strip().split()[-1])
            elif row.strip() == "add y w":
                row = next(f)
                dy = int(row.strip().split()[-1])
                if const:
                    a, b = y.pop()
                    constraints[a] = (digit, x + b)
                else:
                    y.append((digit, dy))
    resolve(constraints)
    to_int(constraints)


def resolve(constraints):
    for i, c in enumerate(constraints):
        if type(c) == tuple:
            a, b = c
            if b < 0:
                constraints[i] = 1 - b
                constraints[a] = 1
            else:
                constraints[i] = 1
                constraints[a] = 1 + b


def to_int(constraints):
    print("".join(map(str, constraints)))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("f", type=str)
    args = parser.parse_args()
    main()
