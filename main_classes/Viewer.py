from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

from PyQt5.QtOpenGL import *

from helpers import Init_Figures as init
from main_classes import Interaction, Primitives, Scene

import numpy as np
from numpy.linalg import inv, norm


class Viewer(QGLWidget):
    def __int__(self, parent=None):
        QGLWidget.__init__(self, parent)
        self.create_interface()
        self.create_opengl()
        self.create_scene()
        self.create_interaction()
        init.init_primitives()

    def create_interface(self):
        ''' Создание рабочего окна '''
        glutInit()
        glutInitWindowSize(800, 600)
        glutCreateWindow('My 3D Renderer')
        glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
        glutDisplayFunc(self.render)

    def create_opengl(self):
        ''' Создание состояния для OpenGL'''

        ''' Задание матриц'''
        self.inverse_model_view = np.identity(4)  # размерность матрицы
        self.model_view = np.identity(4)

        ''' Отсечение задних граней'''
        glEnable(GL_CULL_FACE)
        glCullFace(GL_BACK)
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LESS)

        ''' Создание источника света '''
        glEnable(GL_LIGHT0)
        glLightfv(GL_LIGHT0, GL_POSITION, GLfloat_4(0, 0, 1, 0))
        glLightfv(GL_LIGHT0, GL_SPOT_DIRECTION, GLfloat_3(0, 0, -1))

        '''Раскрашивание объектов'''
        glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
        glEnable(GL_COLOR_MATERIAL)
        glClearColor(0.4, 0.4, 0.4, 0.0)

    def create_scene(self):
        ''' создание сцены и начальных объектов'''
        self.scene = Scene.Scene()
        self.create_sample_scene()

    def create_sample_scene(self):
        cube = Primitives.Cube()
        cube.translate(2, 0, 2)
        cube.color_index = 2
        self.scene.add_figure(cube)

        sphere = Primitives.Sphere()
        sphere.translate(-2, 0, 2)
        sphere.color_index = 3
        self.scene.add_figure(sphere)

        hierarchical_node = Primitives.SnowFigure()
        hierarchical_node.translate(-2, 0, -2)
        self.scene.add_figure(hierarchical_node)

    def create_interaction(self):
        ''' взаимодействие с пользователем '''
        self.interaction = Interaction.Interaction()
        self.interaction.register_callback('pick', self.pick)
        self.interaction.register_callback('move', self.move)
        self.interaction.register_callback('place', self.place)
        self.interaction.register_callback('rotate_color', self.rotate_color)
        self.interaction.register_callback('scale', self.scale)
        self.interaction.register_callback('rotate', self.rotate)

    def render(self):
        ''' подготовка к рендерингу '''
        self.create_view()

        '''отключение источников света'''
        glEnable(GL_LIGHTING)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        '''загрузка матрицы для показа объекта от начального состояния мышки'''
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        loc = self.interaction.translation
        glTranslated(loc[0], loc[1], loc[2])
        glMultMatrixf(self.interaction.trackball.matrix)

        '''сохранение инферсии текущего вида модели'''
        current_model_view = np.array(glGetFloat(GL_MODELVIEW_MATRIX))
        self.model_view = np.transpose(current_model_view)
        self.inverse_model_view = inv(np.transpose(current_model_view))

        '''рендеринг сцены (вызывается для всех объектов)'''
        self.scene.render()

        ''' отрисовка координатного пространства '''
        glDisable(GL_LIGHTING)
        glCallList(init.G_OBJ_PLANE)
        glPopMatrix()

        '''очистка буферов для отрисовки сцены'''
        glFlush()

    def create_view(self):
        '''инициализация проекционной матрицы'''
        xSize, ySize = glutGet(GLUT_WINDOW_WIDTH), glutGet(GLUT_WINDOW_HEIGHT)
        aspect_ratio = float(xSize) / float(ySize)

        '''Загрузка проекционной матрицы'''
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        glViewport(0, 0, xSize, ySize)
        gluPerspective(70, aspect_ratio, 0.1, 1000.0)
        glTranslated(0, 0, -15)

    def get_ray(self, x, y):
        ''' получаем "луч", соединяющий координату, на к-ой находится
        мышка, и ближайшие координаты фигуры(лучше сказать узла)'''
        self.create_view()

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        start = np.array(gluUnProject(x, y, 0.001))
        end = np.array(gluUnProject(x, y, 0.999))

        direction = end - start
        direction /= norm(direction)  # нормаль

        return start, direction

    def pick(self, x, y):
        start, direction = self.get_ray(x, y)
        self.scene.pick(start, direction, self.model_view)

    def move(self, x, y):
        '''перемещение объекта для пользователя (на сцене)'''
        start, direction = self.get_ray(x, y)
        self.scene.move_selected(start, direction, self.inverse_model_view)

    def rotate_color(self, forward):
        '''Смена цвета (можно сказать, что мы поворачиваем узел
        на следующий цвет)'''
        self.scene.rotate_selected_color(forward)

    def scale(self, up):
        self.scene.scale_selected(up)

    def rotate(self, x, y):
        start, direction = self.get_ray(x, y)
        self.scene.rotate(start, direction, self.inverse_model_view)

    def place(self, shape, x, y):
        '''Расположение нового примитива'''
        start, direction = self.get_ray(x, y)
        self.scene.place(shape, start, direction, self.inverse_model_view)

    def main_loop(self):
        ''' цикл самой программы '''
        glutMainLoop()
