import numpy as np
from src import Node

class Apoio:

    list_apoios = []

    def __init__(self, gl, node = None, ** kwargs):

        self.glx = gl[0]
        self.gly = gl[1]
        self.glz = gl[2]
            
        if 'x' and 'y' and 'z' in kwargs:

            self.x = float(kwargs['x'])
            self.y = float(kwargs['y'])
            self.z = float(kwargs['z'])

            self.node = self.identif_node(self.x, self.y, self.z)

        else:
            self.node = node

            self.x = self.node.x
            self.y = self.node.y
            self.z = self.node.z

        self.node.ux = 0 if self.glx[0] == 0 else np.nan
        self.node.rx = 0 if self.glx[1] == 0 else np.nan
        self.node.uy = 0 if self.gly[0] == 0 else np.nan
        self.node.ry = 0 if self.gly[1] == 0 else np.nan
        self.node.uz = 0 if self.glz[0] == 0 else np.nan
        self.node.rz = 0 if self.glz[1] == 0 else np.nan
        
        self.indice = self.node.indice
        
        Apoio.list_apoios.append(self)

        node.get_displacement_vector()
    
    def identif_node(self, x, y, z):
        for idx, iter_node in enumerate(nd.Node.list_nodes):
            if iter_node.x == x and iter_node.y == y:
                ident_node = iter_node
        
        return ident_node