from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import math


class Viewer(object):
    def __init__(self):
        self.angle = 0.0
        self.number_of_lines = 500
        self.rotation = 1.0
        self.coordinates = [0.0, 0.0]
        self.waves_counter = 0
        self.create_interface()

    def create_interface(self):
        glutInit()
        glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGBA)
        glutInitWindowPosition(200, 200)
        glutInitWindowSize(600, 600)
        glutCreateWindow("Waving flag")
        self.create_animation()

    def create_animation(self):
        glClearColor(1.0, 1.0, 1.0, 1.0)
        glOrtho(-5.0, 5.0, -5.0, 5.0, -5.0, 5.0)  # на отдалении объект никак не меняется
        glutDisplayFunc(self.draw)
        glutReshapeFunc(self.proportion)
        glutTimerFunc(0, self.animation, 0)

    def main_loop(self):
        glutMainLoop()

    def proportion(self, width, height):
        if height == 0:
            height = 1
        ratio = float(width) / height
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, ratio, 500, 500)
        glMatrixMode(GL_MODELVIEW)

    def draw_flag(self):
        glBegin(GL_LINE_STRIP)
        glColor3ub(181, 67, 204)
        for i in range(self.number_of_lines + 1):
            a = float(i) / float(self.number_of_lines) * 3.15 * (3.5 * self.rotation)
            self.coordinates[0] = a * 2 - 5
            self.coordinates[1] = math.cos(self.coordinates[0]) / 2 + 5
            glVertex2f(self.coordinates[0], self.coordinates[1])
            self.coordinates[0] = a * 2 - 5
            self.coordinates[1] = math.cos(self.coordinates[0]) / 2 - 5
            glVertex2f(self.coordinates[0], self.coordinates[1])
        glEnd()

    def draw_edges_helper(self):
        glBegin(GL_QUADS)
        glColor3ub(255, 255, 255)

    def draw(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLineWidth(3)
        glPushMatrix()
        glScalef(0.3, 0.3, 1.0)
        glRotatef(5, 0, 0, 1)
        glTranslatef(self.angle, 0, 0)

        self.draw_flag()
        glPopMatrix()

        self.draw_edges_helper()
        glVertex2f(-5, 5)
        glVertex2f(-1.35, 5)
        glVertex2f(-1.35, -5)
        glVertex2f(-5, -5)
        glEnd()
        self.draw_edges_helper()
        glVertex2f(5, 5)
        glVertex2f(5.0, -5)
        glVertex2f(2.0, -5)
        glVertex2f(2.0, 5)
        glEnd()

        glutSwapBuffers()

    def animation(self, value):
        self.angle -= 0.5
        self.rotation += 0.03
        self.waves_counter += 1
        if self.waves_counter == 13:
            self.angle += 6.5
            self.waves_counter = 0
            self.rotation = 1.0
        glutTimerFunc(100, self.animation, 0)
        glutPostRedisplay()


viewer = Viewer()
viewer.main_loop()
