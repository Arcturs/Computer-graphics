import numpy as np
from numpy.linalg import inv
import random

from helpers import Colour, Polygon, Transformations as t

from OpenGL.GL import *


class Node(object):
    def __init__(self):
        self.color_index = random.randint(Colour.color.MIN_COLOR, Colour.color.MAX_COLOR)
        self.polygon = Polygon.Polygon([0.0, 0.0, 0.0], [0.5, 0.5, 0.5])  # ограничивающий параллелипипед, в к-ом находится узел
        self.translation_matrix = np.identity(4)  # создание матрицы размерностью 4
        self.rotating_matrix = np.identity(4)
        self.scaling_matrix = np.identity(4)
        self.selected = False

    def render(self):
        glPushMatrix()
        glMultMatrixf(np.transpose(self.translation_matrix))
        glMultMatrixf(self.scaling_matrix)
        glMultMatrixf(self.rotating_matrix)
        current_color = Colour.color.COLORS[self.color_index]
        glColor3f(current_color[0], current_color[1], current_color[2])
        if self.selected:
            glMaterialfv(GL_FRONT, GL_EMISSION, [0.3, 0.3, 0.3])  # излучение света, если фигура выбрана

        self.render_self()

        if self.selected:
            glMaterialfv(GL_FRONT, GL_EMISSION, [0.0, 0.0, 0.0])
        glPopMatrix()

    def render_self(self):
        raise NotImplementedError()

    def pick(self, start, direction, mat):
        '''возвращает пересек ли "луч" объект'''
        newmat = np.dot(  # перемножение (в данном случае матриц)
            np.dot(mat, self.translation_matrix),
            inv(self.scaling_matrix),
            inv(self.rotating_matrix)
        )
        results = self.polygon.ray_hit(start, direction, newmat)
        return results

    def select(self, select=None):
        '''Переключает выбранное состояние'''
        if select is not None:
            self.selected = select
        else:
            self.selected = not self.selected

    def rotate_color(self, forwards):
        self.color_index += 1 if forwards else -1
        if self.color_index > Colour.color.MAX_COLOR:
            self.color_index = Colour.color.MIN_COLOR
        if self.color_index < Colour.color.MIN_COLOR:
            self.color_index = Colour.color.MAX_COLOR

    def rotate(self, x, y, z):
        self.rotating_matrix = np.dot(
            self.rotating_matrix, t.rotate([x, y, z])
        )

    def scale(self, up):
        s = 1.1 if up else 0.9
        self.scaling_matrix = np.dot(self.scaling_matrix, t.scaling([s, s, s]))
        self.polygon.scale(s)

    def translate(self, x, y, z):
        self.translation_matrix = np.dot(
            self.translation_matrix, t.translation([x, y, z])
        )
