import matplotlib.pyplot as plt
import math
import input_checker
from matplotlib.patches import Polygon
from abc import ABC, abstractmethod


class GeometricFigure(ABC):
    @abstractmethod
    def countArea(self):
        pass


class FigureColor:
    def __init__(self, color):
        self._color = color

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, color):
        self._color = color


class Trapezoid(GeometricFigure):
    name = "Равнобедренная трапеция"

    def __init__(self, a, b, angle_deg, color, caption):
        """
        :param a: длина нижнего основания
        :param b: длина боковой стороны
        :param angle_deg: угол между основанием и боковой стороной (в градусах)
        :param color: цвет заливки
        :param caption: подпись под фигурой
        """
        self.a = a
        self.b = b
        self.angle_deg = angle_deg
        self.color = FigureColor(color)
        self.caption = caption

        self.angle_rad = math.radians(angle_deg)

        self.h = b * math.sin(self.angle_rad)  # height
        self.dx = b * math.cos(self.angle_rad)  # horizontal move
        self.c = a - 2 * self.dx  # upper base

        # coordinates
        self.vertices = [
            (0, 0),                   # lower left corner
            (a, 0),                   # lower right corner
            (a - self.dx, self.h),    # upper right corner
            (self.dx, self.h)         # upper left corner
        ]

    def drawTrapezoid(self):
        """Drawing trapezoid"""

        fig, ax = plt.subplots()
        polygon = Polygon(self.vertices, closed=True, fill=True, color=self.color.color)
        ax.add_patch(polygon)

        padding = max(self.a, self.h) * 0.2
        ax.set_xlim(-padding, self.a + padding)
        ax.set_ylim(-padding, self.h + padding)
        ax.set_aspect('equal')
        plt.axis('off')

        plt.text(self.a / 2, -padding / 2, self.caption,
                 ha='center', fontsize=13, fontfamily='serif')

        plt.savefig("trapezoid.png")
        plt.show()

    def countArea(self):
        """Count square"""
        return ((self.a + self.c) / 2) * self.h

    def getParams(self):
        """returns info"""
        return f"Цвет: {self.color.color}\nПлощадь: {self.countArea():.2f}"

    @classmethod
    def getName(cls):
        return cls.name


def task4():
    print("Введите параметры равнобедренной трапеции:")
    a = input_checker.input_checker("Длина нижнего основания (a): ", float, 1)
    b = input_checker.input_checker("Длина боковой стороны (b): ", float, 1)
    angle_deg = input_checker.input_checker("Угол между основанием и боковой стороной (в градусах): ", int, 1)
    color = input("Цвет на английском (например 'blue'): ")
    caption = input("Подпись к фигуре: ")

    trapezoid = Trapezoid(a, b, angle_deg, color, caption)
    print(trapezoid.getParams())
    trapezoid.drawTrapezoid()