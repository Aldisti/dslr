
from datetime import datetime
from math import sqrt
from sys import argv
from re import match





if len(argv) != 2:
    print(f"Error: usage {argv[0]} <dataset>")
    exit(1)

FILE = argv[1]

with open(FILE) as file:
    lines = file.readlines()

data = {}
headers = []





def to_date(n: int) -> str:
    return datetime.fromtimestamp(n).strftime("%d-%m-%Y")

def to_unix(date: str, format: str="%Y-%m-%d") -> int:
    return datetime.strptime(date, format).timestamp()

def is_num(s: str) -> bool:
    return bool(match(r'^[-+]?\d*\.?\d+([eE][-+]?\d+)?$', s))





for header in lines[0].split(','):
    headers.append(header.lower().strip())
    data[header.lower().strip()] = []

for line in lines[1:]:
    line = line.split(',')
    for i, value in enumerate(line):
        if i == 0 or value == "" or not is_num(value):
            continue
        data[headers[i]].append(float(value))





def ft_mean(values: list[int|float]) -> float:
    return sum(values) / len(values)

def ft_std(values: list[int|float]) -> float:
    mean = ft_mean(values)
    summation = 0
    for n in values:
        summation += (n - mean) ** 2
    return sqrt(summation / (len(values) - 1))

def ft_min(values: list[int|float]) -> float:
    minimum = values[0]
    for value in values:
        if value < minimum:
            minimum = value
    return minimum

def ft_q(values: list[int|float], perc: float) -> float:
    values = sorted(values)
    index = perc * (len(values) + 1)
    if index.is_integer():
        return values[int(index)]
    i_low = int(index)
    i_high = int(index) + 1
    return values[i_low] + (index - i_low) * (values[i_high] - values[i_low])

def ft_q1(values: list[int|float]) -> float:
    return ft_q(values, 0.25)

def ft_q2(values: list[int|float]) -> float:
    return ft_q(values, 0.5)

def ft_q3(values: list[int|float]) -> float:
    return ft_q(values, 0.75)

def ft_max(values: list[int|float]) -> float:
    maximum = values[0]
    for value in values:
        if value > maximum:
            maximum = value
    return maximum



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


