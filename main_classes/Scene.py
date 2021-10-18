import numpy as np
import sys

from main_classes import Primitives as p


class Scene(object):
    PLACE_DEPTH = 13.0  # глубина размещения камеры

    def __init__(self):
        self.node_list = list()  # лист фигур для показа
        self.selected_node = None

    def add_figure(self, node):
        ''' добавление новой фигуры '''
        self.node_list.append(node)

    def render(self):
        ''' рендеринг '''
        for node in self.node_list:
            node.render()

    def pick(self, start, direction, mat):
        ''' mat - обратная матрица model_view
        Определяем какой из ближайших узлов пронзил наш луч'''
        if self.selected_node is not None:
            self.selected_node.select(False)
            self.selected_node = None

        mindist = sys.maxsize
        closest_node = None
        for node in self.node_list:
            hit, distance = node.pick(start, direction, mat)
            if hit and distance < mindist:
                mindist, closest_node = distance, node

        '''здесь луч попал в какой-то узел'''
        if closest_node is not None:
            closest_node.select()
            closest_node.depth = mindist
            closest_node.selected_loc = start + direction * mindist
            self.selected_node = closest_node

        '''
        Взять за основу pick, потом перемножаем матрицы для scale 
        '''

    def rotate_selected_color(self, forwards):
        if self.selected_node is None:
            return
        self.selected_node.rotate_color(forwards)

    def scale_selected(self, up):
        if self.selected_node is None:
            return
        self.selected_node.scale(up)

    def rotate(self, x, y, inv_modelview):
        if self.selected_node is None:
            return
        node = self.selected_node
        depth = node.depth
        oldloc = node.selected_loc

        newloc = x + y * depth

        translation = newloc - oldloc
        pre_tran = np.array([translation[0], translation[1], translation[2], 0])
        translation = inv_modelview.dot(pre_tran)

        node.rotate(translation[0], translation[1], translation[2])
        node.selected_loc = newloc

    def move_selected(self, start, direction, inv_modelview):
        ''' перемещение узла (принцип схож с выбором ближайшего узла)'''
        if self.selected_node is None:
            return

        '''Глубина и расположение выбранного узла'''
        node = self.selected_node
        depth = node.depth
        oldloc = node.selected_loc

        '''узел будет располагаться на том же луче'''
        newloc = start + direction * depth

        '''Преобразование перемещения с помощью матрицы'''
        translation = newloc - oldloc
        pre_tran = np.array([translation[0], translation[1], translation[2], 0])
        translation = inv_modelview.dot(pre_tran)

        node.translate(translation[0], translation[1], translation[2])
        node.selected_loc = newloc

    def place(self, shape, start, direction, inv_modelview):
        '''Размещение нового узла под курсором мыши +
        перемещение узла на вектор'''
        new_node = None
        if shape == 'sphere':
            new_node = p.Sphere()
        elif shape == 'cube':
            new_node = p.Cube()
        elif shape == 'figure':
            new_node = p.SnowFigure()

        translation = start + direction * self.PLACE_DEPTH

        pre_tran = np.array(translation[0], translation[1], translation[2])
        translation = inv_modelview.dot(pre_tran)

        new_node.translate(translation[0], translation[1], translation[2])
