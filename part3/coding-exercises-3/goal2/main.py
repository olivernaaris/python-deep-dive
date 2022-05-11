from random import seed, choices
from collections import Counter

eye_colors = ("amber", "blue", "brown", "gray", "green", "hazel", "red", "violet")


class Person:
    def __init__(self, eye_color):
        self.eye_color = eye_color


seed(0)
persons = [Person(color) for color in choices(eye_colors[2:], k = 50)]


def count_eye_colors(persons, possible_eye_colors):
    counts = Counter({color: 0 for color in possible_eye_colors})
    counts.update(p.eye_color for p in persons)
    return counts


print(count_eye_colors(persons, eye_colors))
