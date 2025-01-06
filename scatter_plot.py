
from matplotlib import pyplot as plt
from matplotlib.patches import Patch
from sys import argv

from library import *


class Alumn:
    HOUSES: set[str] = set()
    COURSES: list[str] = list()

    def __init__(self, **kwargs):
        self.index: int = kwargs.pop('index', -1)
        self.house: str = kwargs.pop('hogwarts house', None)
        if 'birthday' in kwargs:
            self.birthday: int = to_unix(kwargs.pop('birthday'))
        self.first_name = kwargs.pop('first name', None)
        self.last_name = kwargs.pop('last name', None)
        self.hand: str = kwargs.pop('best hand').lower()
        self.courses: dict[str:float] = dict()

        for course, value in kwargs.items():
            if value == "" or not is_num(value):
                continue
            self.courses[course] = float(value)

            if course not in Alumn.COURSES:
                Alumn.COURSES.append(course)

        if self.house is not None and self.house not in Alumn.HOUSES:
            Alumn.HOUSES.add(self.house)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name} {self.house} {self.hand} {self.courses}"


HOUSE_COLORS = {
    'ravenclaw': 'purple',
    'slytherin': 'green',
    'gryffindor': 'red',
    'hufflepuff': 'blue',
}


def smallest_mse(alumni: list[Alumn]) -> tuple[str, str]:
    smallest = None
    for course in Alumn.COURSES:
        values = normalize_values([alumn.courses.get(course) for alumn in alumni if course in alumn.courses])
        for sub_course in Alumn.COURSES:
            if sub_course <= course:
                continue
            sub_values = normalize_values([alumn.courses.get(sub_course) for alumn in alumni if sub_course in alumn.courses])
            mse = ft_mse(values, sub_values, True)

            if smallest is None or mse < smallest[0]:
                smallest = (mse, (course, sub_course))
    return smallest[1]


def main() -> None:
    if len(argv) != 2:
        print(f"Error: usage {argv[0]} <dataset>")
        exit(1)

    FILE = argv[1]

    with open(FILE) as file:
        lines = file.readlines()

    headers = []

    for header in lines[0].split(','):
        headers.append(header.lower().strip())

    alumni = []
    for line in lines[1:]:
        line = {headers[i]: value.lower().strip() for i, value in enumerate(line.split(','))}
        alumni.append(Alumn(**line))

    Alumn.COURSES.sort()


    similar_courses = smallest_mse(alumni)

    fig, axes = plt.subplots(nrows=3, ncols=5, figsize=(18, 10))
    axes = axes.flatten()

    for i in range(len(Alumn.COURSES)):
        axe = axes[i]
        course = Alumn.COURSES[i]

        course_values = [alumn.courses.get(course) for alumn in alumni if course in alumn.courses]
        house_values = {house: [alumn.courses.get(course) for alumn in alumni if course in alumn.courses and alumn.house == house] for house in Alumn.HOUSES}
        house_values = {house: normalize_values(values, ft_max(course_values), ft_min(course_values)) for house, values in house_values.items()}
        house_values = dict(sorted(house_values.items(), key=lambda item: len(item)))

        axe.set_title(course)
        for house, values in house_values.items():
            axe.scatter(
                range(len(values)),
                (values),
                color=HOUSE_COLORS[house]
            )

        if course in similar_courses:
            axe.set_facecolor('lightyellow')


    for i in range(len(Alumn.COURSES), len(axes)):
        fig.delaxes(axes[i])

    fig.tight_layout()
    legend_colors = [Patch(facecolor=color, label=house.capitalize()) for house, color in HOUSE_COLORS.items()]
    fig.legend(handles=legend_colors, loc='lower right', fontsize=16)

    plt.show()

if __name__ == '__main__':
    main()
