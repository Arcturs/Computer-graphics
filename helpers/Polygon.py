import numpy as np
import math
from helpers import Init_Figures as init
from OpenGL.GL import *


EPSILON = 0.000001


class Polygon(object):
    def __init__(self, center, size):
        self.center = np.array(center)
        self.size = np.array(size)

    def scale(self, scale):
        self.size *= scale

    def ray_hit(self, origin, direction, model_matrix):
        ''' если луч дошел до полигона'''
        polygon_min = self.center - self.size
        polygon_max = self.center + self.size
        t_min = 0.0
        t_max = 100000.0

        obb_pos_worldspace = np.array([model_matrix[0, 3], model_matrix[1, 3], model_matrix[2, 3]])
        delta = obb_pos_worldspace - origin

        '''Проверка пересечения плоскости, перпендикулярной оси X'''
        xaxis = np.array((model_matrix[0, 0], model_matrix[0, 1], model_matrix[0, 2]))

        e = np.dot(xaxis, delta)
        f = np.dot(direction, xaxis)
        if math.fabs(f) > 0.0 + EPSILON:
            t1 = (e + polygon_min[0]) / f
            t2 = (e + polygon_max[0]) / f
            if t1 > t2:
                t1, t2 = t2, t1
            if t2 < t_max:
                t_max = t2
            if t1 > t_min:
                t_min = t1
            if t_max < t_min:
                return False, 0
        else:
            if (-e + polygon_min[0] > 0.0 + EPSILON) or (-e + polygon_max[0] < 0.0 - EPSILON):
                return False, 0

        yaxis = np.array((model_matrix[1, 0], model_matrix[1, 1], model_matrix[1, 2]))
        e = np.dot(yaxis, delta)
        f = np.dot(direction, yaxis)
        if math.fabs(f) > 0.0 + EPSILON:
            t1 = (e + polygon_min[0]) / f
            t2 = (e + polygon_max[0]) / f
            if t1 > t2:
                t1, t2 = t2, t1
            if t2 < t_max:
                t_max = t2
            if t1 > t_min:
                t_min = t1
            if t_max < t_min:
                return False, 0
        else:
            if (-e + polygon_min[0] > 0.0 + EPSILON) or (-e + polygon_max[0] < 0.0 - EPSILON):
                return False, 0

        zaxis = np.array((model_matrix[2, 0], model_matrix[2, 1], model_matrix[2, 2]))
        e = np.dot(xaxis, delta)
        f = np.dot(direction, xaxis)
        if math.fabs(f) > 0.0 + EPSILON:
            t1 = (e + polygon_min[0]) / f
            t2 = (e + polygon_max[0]) / f
            if t1 > t2:
                t1, t2 = t2, t1
            if t2 < t_max:
                t_max = t2
            if t1 > t_min:
                t_min = t1
            if t_max < t_min:
                return False, 0
        else:
            if (-e + polygon_min[0] > 0.0 + EPSILON) or (-e + polygon_max[0] < 0.0 - EPSILON):
                return False, 0

        return True, t_min

    def render(self):
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glTranslated(self.center[0], self.center[1], self.center[2])
        glCallList(init.G_OBJ_CUBE)
        glPopMatrix()
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
