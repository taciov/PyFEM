import numpy as np

class CargaPontual:
    def __init__(self, fx, fy, mt, *args, **kwargs):
        self.yype = 'pontual'
        self.fx = fx
        self.fy = fy
        self.mt = mt

        if 'x' in kwargs:
            self.x = kwargs['x']
        else:
            self.x = args[0]
        if 'y' in kwargs:
            self.x = kwargs['y']
        else:
            self.y = args[1]

class CargaUniforme:
    def __init__(self, qx, qy, mt, *args, **kwargs):
        self.type = 'uniforme'

        if 'x1' and 'y1' in kwargs:
            self.x1 = kwargs['x1']
            self.y1 = kwargs['y1']
        else:
            self.x1 = args[0][0]
            self.y1 = args[0][1]
        
        if 'x2' and 'y2' in kwargs:
            self.x2 = kwargs['x2']
            self.y2 = kwargs['y2']
        else:
            self.x2 = args[1][0]
            self.y2 = args[1][1]
        
        self.qx = qx
        self.qy = qy
        self.mt = mt

        # self.length = np.sqrt((self.x2 - self.x1) ** 2 + (self.y2 - self.y1) ** 2)
        self.length = ((self.x2 - self.x1) ** 2 + (self.y2 - self.y1) ** 2) ** (1 / 2)
    
    def definir_nos(self, lista_nos):
        for node in lista_nos:
            if node.x == self.x1 and node.y == self.y1:
                self.node1 = node
                self.node1_idx = node.indice
            if float(node.x) == float(self.x2) and float(node.y) == float(self.y2):
                self.node2 = node
                self.node2_idx = node.indice
        self.lista_nos = []
        for node in lista_nos:
            if (node.indice >= self.node1.indice and node.indice <= self.node2.indice) or (node.indice >= self.node2.indice and node.indice <= self.node1.indice):
                self.lista_nos.append(node)

class Apoio:
    def __init__(self, xy, *args):
        self.x = xy[0]
        self.y = xy[1]
        self.gl = args
        self.fx = args[0]
        self.fy = args[1]
        self.mt = args[2]
