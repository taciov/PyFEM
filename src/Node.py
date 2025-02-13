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

class NodeGeneral:

    list_nodes = []

    def __init__(self, x, y, z):

        NodeGeneral.list_nodes.append(self)
        self.indice = len(NodeGeneral.list_nodes)
        self.lista_graus = [6 * self.indice - 5, 
                            6 * self.indice - 4, 
                            6 * self.indice - 3,
                            6 * self.indice - 2, 
                            6 * self.indice - 1, 
                            6 * self.indice]

        self.x = x
        self.y = y
        self.z = z

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
        if 'fz' in kwargs:
            self.fz = float(kwargs['fz'])
        else:
            self.fz = 0
        if 'mx' in kwargs:
            self.mx = float(kwargs['mx'])
        else:
            self.mx = 0
        if 'my' in kwargs:
            self.my = float(kwargs['my'])
        else:
            self.my = 0
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
        if 'uz' in kwargs:
            self.uz = float(kwargs['uz'])
        else:
            self.uz = np.nan
        
        if 'rx' in kwargs:
            self.rx = float(kwargs['rx'])
        else:
            self.rx = np.nan
        if 'ry' in kwargs:
            self.ry = float(kwargs['ry'])
        else:
            self.ry = np.nan
        if 'rz' in kwargs:
            self.rz = float(kwargs['rz'])
        else:
            self.rz = np.nan
    
    @classmethod
    def clear_list_nodes(cls):
        cls.list_nodes = []

    def __str__(self) -> str:
        return {

            'x' : self.x,
            'y' : self.y,
            'z' : self.z
        }