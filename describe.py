
from library import *
from sys import argv


methods = {
    'Count': len,
    'Mean': ft_mean,
    'Std': ft_std,
    'Min': ft_min,
    '25%': ft_q1,
    '50%': ft_q2,
    '75%': ft_q3,
    'Max': ft_max,
}

@catch
def main() -> None:

    if len(argv) != 2:
        print(f"Error: usage {argv[0]} <dataset>")
        exit(1)

    FILE = argv[1]

    with open(FILE) as file:
        lines = file.readlines()

    data = {}
    headers = []


    for header in lines[0].split(','):
        headers.append(header.lower().strip())
        data[header.lower().strip()] = []

    for line in lines[1:]:
        line = line.split(',')
        for i, value in enumerate(line):
            if i == 0 or value == "" or not is_num(value):
                continue
            data[headers[i]].append(float(value))

    PAD = 20

    for header in list(data.keys()):
        if data[header] == []:
            del data[header]
            continue
        if len(header) > PAD:
            PAD = len(header)

    s = " " * PAD
    for header in data.keys():
        if data[header] == []:
            continue
        s += f"{header:>{PAD}}"
    print(s)

    for method, fun in methods.items():
        s = f"{method:<{PAD}}"
        for header in data.keys():
            if data[header] == []:
                continue
            s += f"{round(fun(data[header]), 5):>{PAD}}"
        print(s)

if __name__ == '__main__':
    main()
