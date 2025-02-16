# from src import Node as nd

import sympy as sp
import numpy as np

class Barra:

    list_bars = []
    

    def __init__(self, E, A, I, *args, **kwargs):

        self.lista_cargas = []
        Barra.list_bars.append(self)
        self.list_nodes = [node for node in args]
        L, self.theta = self.definir_geometria()

        self.ke_ = sp.Matrix([[E * A / L, 0, 0, -E * A / L, 0, 0],
                 [0, 12 * E * I / (L **3), 6 * E * I / (L ** 2), 0, -12 * E * I / (L **3), 6 * E * I / (L ** 2)],
                 [0, 6 * E * I / (L ** 2), 4 * E * I / L, 0, -6 * E * I / (L ** 2), 2 * E * I / L],
                 [-E * A / L, 0, 0, E * A / L, 0, 0],
                 [0, -12 * E * I / (L **3), -6 * E * I / (L ** 2), 0, 12 * E * I / (L **3), -6 * E * I / (L ** 2)],
                 [0, 6 * E * I / (L ** 2), 2 * E * I / L, 0, -6 * E * I / (L ** 2), 4 * E * I / L]
                 ])
        c = sp.cos(self.theta)
        s = sp.sin(self.theta)
        self.T = sp.Matrix([[c, s, 0, 0, 0, 0,],
                        [-s, c, 0, 0, 0, 0,],
                        [0, 0, 1, 0, 0, 0],
                        [0, 0, 0, c, s, 0],
                        [0, 0, 0, -s, c, 0],
                        [0, 0, 0, 0, 0, 1]
        ])
        self.A, self.E, self.L, self.I = A, E, L, I
        self.ke = self.T.T * self.ke_ * self.T

        self.get_forces_vector()
        self.atribuir_graus()

    def get_forces_vector(self):
        node1, node2 = self.list_nodes
        self.f = np.array([node1.fx, node1.fy, node1.mz, node2.fx, node2.fy, node2.mz])  

    def definir_geometria(self):
        node1, node2 = self.list_nodes
        x1, y1, x2, y2 = node1.x, node1.y, node2.x, node2.y
        length = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        if ((x2 - x1) == 0) and ((y2 - y1) > 0):
            theta = np.pi / 2
        elif ((x2 - x1) == 0) and ((y2 - y1) < 0):
            theta = 3 * np.pi / 2
        elif ((y2 - y1) == 0) and ((x2 - x1) > 0):
            theta = 0
        elif ((y2 - y1) == 0) and ((x2 - x1) < 0):
            theta = np.pi
        else:
            theta = np.arctan((y2 - y1) / (x2 - x1))
        
        return length, theta

    def atribuir_nos(self, primeiro_no, segundo_no):
        self.list_nodes = [primeiro_no, segundo_no]

    def atribuir_graus(self):
        self.lista_graus = []
        for node in self.list_nodes:
            for idx, grau in enumerate(node.lista_graus):
                self.lista_graus.append(grau) if idx not in [1, 3, 4] else None
        print(self.lista_graus)
        self.ke = self.ke.row_insert(0, sp.Matrix([self.lista_graus]))
        lista_graus_temp = self.lista_graus.copy()
        lista_graus_temp.append(0)
        self.ke = self.ke.col_insert(0, sp.Matrix(sorted(lista_graus_temp)))
    
    @classmethod
    def clear_list_bars(cls):
        cls.list_bars = []