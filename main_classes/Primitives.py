from OpenGL.GL import *
import numpy as np

from main_classes import Node
from helpers import Colour, Init_Figures as init, Polygon, Transformations as t


class Primitive(Node.Node):
     def __init__(self):
         super(Primitive, self).__init__()
         self.call_list = None

     def render_self(self):
         glCallList(self.call_list)


class Sphere(Primitive):
    def __init__(self):
        super(Sphere, self).__init__()
        self.call_list = init.G_OBJ_SPHERE


class Cube(Primitive):
    def __init__(self):
        super(Cube, self).__init__()
        self.call_list = init.G_OBJ_CUBE


class HierarchicalNode(Node.Node):
    ''' класс более сложных фигур (иерархические узлы)'''
    def __init__(self):
        super(HierarchicalNode, self).__init__()
        self.child_nodes = []

    def render_self(self):
        for child in self.child_nodes:
            child.render()


class SnowFigure(HierarchicalNode):
    def __init__(self):
        super(SnowFigure, self).__init__()
        self.child_nodes = [Sphere(), Sphere(), Sphere()]
        self.child_nodes[0].translate(0, -0.6, 0)
        self.child_nodes[1].translate(0, 0.1, 0)
        self.child_nodes[1].scaling_matrix = np.dot(
            self.scaling_matrix, t.scaling([0.8, 0.8, 0.8])
        )
        self.child_nodes[2].translate(0, 0.75, 0)
        self.child_nodes[2].scaling_matrix = np.dot(
            self.scaling_matrix, t.scaling([0.7, 0.7, 0.7])
        )
        for child_node in self.child_nodes:
            child_node.color_index = Colour.color.MIN_COLOR
        self.polygon = Polygon.Polygon([0.0, 0.0, 0.0], [0.5, 1.1, 0.5])
