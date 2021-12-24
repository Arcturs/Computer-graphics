from OpenGL.GL import *
from OpenGL.GLUT import *
import time


class Viewer(object):
    def __init__(self):
        self.cube_angels = [0, 0, 0, 0]
        self.cube_size = 150
        self.window_size = 300
        self.rotation = True
        self.create_interface()

    def create_interface(self):
        glutInit()
        glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
        glutInitWindowSize(self.window_size * 2, self.window_size * 2)
        glutInitWindowPosition(200, 200)
        glutCreateWindow("Cube rotation")
        glutDisplayFunc(self.draw)
        glRotatef(55, 1, 0, 0)
        glRotatef(45, 0, 0, 1)
        glutTimerFunc(20, self.animation, 0)
        self.create_animation()

    def create_animation(self):
        glClearColor(1.0, 1.0, 1.0, 1.0)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(-self.window_size, self.window_size, -self.window_size,
                self.window_size, -self.window_size, self.window_size)
        glMatrixMode(GL_MODELVIEW)

    def main_loop(self):
        glutMainLoop()

    def draw_carcass_helper(self, width):
        glLineWidth(width)
        glBegin(GL_LINES)
        glColor3d(0, 0, 0)

    def draw_carcass(self):
        self.draw_carcass_helper(4)
        glVertex3f(-self.cube_size, -self.cube_size, -self.cube_size)
        glVertex3f(self.cube_size, self.cube_size, -self.cube_size)
        glVertex3f(self.cube_size, -self.cube_size, -self.cube_size)
        glVertex3f(-self.cube_size, self.cube_size, -self.cube_size)
        glEnd()
        self.draw_carcass_helper(3)
        glVertex3f(-self.cube_size, -self.cube_size, self.cube_size)
        glVertex3f(self.cube_size, self.cube_size, self.cube_size)
        glVertex3f(self.cube_size, -self.cube_size, self.cube_size)
        glVertex3f(-self.cube_size, self.cube_size, self.cube_size)
        glEnd()
        self.draw_carcass_helper(3)
        glVertex3f(self.cube_size, -self.cube_size, -self.cube_size)
        glVertex3f(-self.cube_size, -self.cube_size, self.cube_size)
        glVertex3f(self.cube_size, -self.cube_size, self.cube_size)
        glVertex3f(-self.cube_size, -self.cube_size, -self.cube_size)
        glEnd()
        self.draw_carcass_helper(3)
        glVertex3f(self.cube_size, self.cube_size, -self.cube_size)
        glVertex3f(-self.cube_size, self.cube_size, self.cube_size)
        glVertex3f(self.cube_size, self.cube_size, self.cube_size)
        glVertex3f(-self.cube_size, self.cube_size, -self.cube_size)
        glEnd()
        self.draw_carcass_helper(3)
        glVertex3f(-self.cube_size, -self.cube_size, -self.cube_size)
        glVertex3f(-self.cube_size, self.cube_size, self.cube_size)
        glVertex3f(-self.cube_size, self.cube_size, -self.cube_size)
        glVertex3f(-self.cube_size, -self.cube_size, self.cube_size)
        glEnd()
        self.draw_carcass_helper(3)
        glVertex3f(self.cube_size, -self.cube_size, -self.cube_size)
        glVertex3f(self.cube_size, self.cube_size, self.cube_size)
        glVertex3f(self.cube_size, self.cube_size, -self.cube_size)
        glVertex3f(self.cube_size, -self.cube_size, self.cube_size)
        glEnd()

    def draw_cube(self):
        glEnable(GL_LINE_STIPPLE)
        glLineWidth(1)
        glBegin(GL_LINE_LOOP)
        glColor3d(0, 0, 0)
        glVertex3f(-self.cube_size, -self.cube_size, -self.cube_size)
        glVertex3f(self.cube_size, -self.cube_size, -self.cube_size)
        glVertex3f(self.cube_size, self.cube_size, -self.cube_size)
        glVertex3f(-self.cube_size, self.cube_size, -self.cube_size)
        glVertex3f(-self.cube_size, -self.cube_size, -self.cube_size)
        glEnd()
        glBegin(GL_LINE_LOOP)
        glColor3d(0, 0, 0)
        glVertex3f(-self.cube_size, -self.cube_size, self.cube_size)
        glVertex3f(self.cube_size, -self.cube_size, self.cube_size)
        glVertex3f(self.cube_size, self.cube_size, self.cube_size)
        glVertex3f(-self.cube_size, self.cube_size, self.cube_size)
        glVertex3f(-self.cube_size, -self.cube_size, self.cube_size)
        glEnd()
        glBegin(GL_LINES)
        glColor3d(0, 0, 0)
        glVertex3f(-self.cube_size, -self.cube_size, self.cube_size)
        glVertex3f(-self.cube_size, -self.cube_size, -self.cube_size)
        glVertex3f(self.cube_size, -self.cube_size, self.cube_size)
        glVertex3f(self.cube_size, -self.cube_size, -self.cube_size)
        glVertex3f(self.cube_size, self.cube_size, self.cube_size)
        glVertex3f(self.cube_size, self.cube_size, -self.cube_size)
        glVertex3f(-self.cube_size, self.cube_size, self.cube_size)
        glVertex3f(-self.cube_size, self.cube_size, -self.cube_size)
        glEnd()

    def draw(self):
        glClear(GL_COLOR_BUFFER_BIT)
        glPushMatrix()  # сдвигает матрицу
        glRotatef(self.cube_angels[0], 1, 0, 0)
        glRotatef(self.cube_angels[1], 0, 1, 0)
        glRotatef(self.cube_angels[2], 0, 0, 1)
        glRotatef(self.cube_angels[3], 1, 0, 0)

        glLineStipple(1, 0X00FF)
        glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_LINE_SMOOTH)

        self.draw_carcass()
        self.draw_cube()

        glDisable(GL_LINE_STIPPLE)
        glDisable(GL_LINE_SMOOTH)
        glPopMatrix() # возвращает в исх. положение
        glutSwapBuffers()

    def animation(self, value):
        if self.cube_angels[0] < 90:
            self.cube_angels[0] += 1
        elif self.cube_angels[1] < 90:
            self.cube_angels[1] += 1
        elif self.cube_angels[2] < 90:
            self.cube_angels[2] += 1
        elif self.cube_angels[3] < 90:
            self.cube_angels[3] += 1
        else:
            self.cube_angels = [0, 0, 0, 0]
        if self.cube_angels[0] == 90 and self.cube_angels[1] == 1:
            time.sleep(0.3)
        if self.cube_angels[1] == 90 and self.cube_angels[2] == 1:
            time.sleep(0.3)
        if self.cube_angels[2] == 90 and self.cube_angels[3] == 1:
            time.sleep(0.3)
        if self.cube_angels[0] == 1:
            time.sleep(0.3)
        glutPostRedisplay()
        glutTimerFunc(10, self.animation, 0)


viewer = Viewer()
viewer.main_loop()
