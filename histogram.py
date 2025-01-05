
from matplotlib import pyplot as plt
from sys import argv

from library import *



COURSE_HEADERS = [
    'arithmancy',
    'astronomy',
    'herbology',
    'defense against the dark arts',
    'divination',
    'muggle studies',
    'ancient runes',
    'history of magic',
    'transfiguration',
    'potions',
    'care of magical creatures',
    'charms',
    'flying',
]

HOUSES = {
    'Ravenclaw': 'purple',
    'Slytherin': 'green',
    'Gryffindor': 'red',
    'Hufflepuff': 'blue',
}

HOUSE_HEADER = 'hogwarts house'


@catch
def main() -> None:
    if len(argv) != 2:
        print(f"Error: usage {argv[0]} <dataset>")
        exit(1)

    FILE = argv[1]

    with open(FILE) as file:
        lines = file.readlines()

    courses = {}
    headers = []

    for header in lines[0].split(','):
        headers.append(header.lower().strip())

    for line in lines[1:]:
        line = line.split(',')
        house = None
        for i, value in enumerate(line):
            header = headers[i]
            if header == HOUSE_HEADER:
                house = value
                continue
            if header not in COURSE_HEADERS or value == "" or not is_num(value):
                continue

            if header not in courses:
                courses[header] = {}
            if house not in courses[header]:
                courses[header][house] = []

            value = float(value)
            courses[header][house].append(value)

    houses = HOUSES
    fig, *plots = plt.subplots(nrows=3, ncols=5)
    for i, axes in enumerate(plots[0]):
        for j, axe in enumerate(axes):
            if i * 5 + j >= len(COURSE_HEADERS):
                break
            course = COURSE_HEADERS[i * 5 + j]
            axe.set_title(course)
            houses = dict(sorted(houses.items(), key=lambda item: -len(set(courses[course][item[0]]))))
            for house in houses.keys():
                axe.hist(
                    (courses[course][house]),
                    color=houses[house],
                    edgecolor=houses[house],
                    label=house,
                    fill=True
                )

    fig.tight_layout()
    plt.show()

if __name__ == '__main__':
    main()
