import numpy as np

class Node:

    list_nodes = []

    def __init__(self, x, y):

        Node.list_nodes.append(self)
        self.indice = len(Node.list_nodes)
        self.lista_graus = [3 * self.indice - 2, 3 * self.indice - 1, 3 * self.indice]
        self.x = x
        self.y = y

        self.set_force()
        self.set_displacement()

    def set_force(self, **kwargs):
        if 'fx' in kwargs:
            self.fx = float(kwargs['fx'])
        else:
            self.fx = 0
        if 'fy' in kwargs:
            self.fy = float(kwargs['fy'])
        else:
            self.fy = 0
        if 'mz' in kwargs:
            self.mz = float(kwargs['mz'])
        else:
            self.mz = 0

    def set_displacement(self, **kwargs):
        if 'ux' in kwargs:
            self.ux = float(kwargs['ux'])
        else:
            self.ux = np.nan
        if 'uy' in kwargs:
            self.uy = float(kwargs['uy'])
        else:
            self.uy = np.nan
        if 'ang' in kwargs:
            self.ang = float(kwargs['ang'])
        else:
            self.ang = np.nan
    
    @classmethod
    def clear_list_nodes(cls):
        cls.list_nodes = []