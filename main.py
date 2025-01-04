
from matplotlib import pyplot as plt
from datetime import datetime

FILE = r'datasets/dataset_train.csv'

with open(FILE) as file:
    lines = file.readlines()

data = {}
headers = []


def to_date(n: int) -> str:
    return datetime.fromtimestamp(n).strftime("%d-%m-%Y")

def to_unix(date: str, format: str="%Y-%m-%d") -> int:
    return datetime.strptime(date, format).timestamp()

def mean(values: list[int|float]) -> float:
    return sum(values) / len(values)



for header in lines[0].split(','):
    header = header.lower()
    if header not in ['index', 'hogwarts house', 'first name', 'last name', 'best hand']:
        data[header] = []
    headers.append(header)

for line in lines[1:]:
    line = line.replace(',,,', ',0,0,').replace(',,', ',0,').split(',')
    for i, value in enumerate(line):
        if headers[i] in ['index', 'hogwarts house', 'first name', 'last name', 'best hand']:
            continue
        if headers[i] == 'birthday':
            value = to_unix(value)
        else:
            try:
                value = float(value)
            except ValueError:
                print(f"|{line}|{value}| is not a number")
        data[headers[i]].append(value)



for header, values in data.items():
    if header in ['index', 'hogwarts house', 'first name', 'last name']:
        continue
    plt.title(header)
    plt.plot(values, range(1, len(values) + 1), 'o')
    if header == 'birthday':
        plt.xticks([min(values), mean(values), max(values)], [to_date(min(values)), to_date(int(mean(values))), to_date(max(values))])
    plt.show()


