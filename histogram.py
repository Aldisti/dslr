
from matplotlib import pyplot as plt
from matplotlib.patches import Patch
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


# @catch
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
    fig, axes = plt.subplots(nrows=3, ncols=5, figsize=(18, 10))
    axes = axes.flatten()

    for i in range(len(COURSE_HEADERS)):
        axe = axes[i]
        course = COURSE_HEADERS[i]

        axe.set_title(course)
        max = ft_max([ft_max(values) for values in courses[course].values()])
        min = ft_min([ft_min(values) for values in courses[course].values()])
        houses = dict(sorted(houses.items(), key=lambda item: -len(set(courses[course][item[0]]))))
        for house in houses.keys():
            axe.hist(
                normalize_values(courses[course][house], max, min),
                color=houses[house],
                edgecolor=houses[house],
                label=house,
                fill=True
            )

    for i in range(len(COURSE_HEADERS), len(axes)):
        fig.delaxes(axes[i])

    fig.tight_layout()
    legend_colors = [Patch(facecolor=color, label=house.capitalize()) for house, color in HOUSES.items()]
    fig.legend(handles=legend_colors, loc='lower right', fontsize=16)

    plt.show()

if __name__ == '__main__':
    main()
