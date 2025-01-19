from src import Node as nd

class Apoio:

    list_apoios = []

    def __init__(self, gl, x = None, y = None, ** kwargs):

        self.glx = gl[0]
        self.gly = gl[1]
        self.glz = gl[2]

        if 'node' in kwargs:
            self.node = kwargs['node']

            self.x = self.node.x
            self.y = self.node.y
            
        else:
            self.x = x
            self.y = y

            self.node = nd.Node(x, y)

        if self.glx == 0:
            self.node.ux = 0
        
        if self.gly == 0:
            self.node.uy = 0

        if self.glz == 0:
            self.node.ang = 0
        
        self.indice = self.node.indice
        
        Apoio.list_apoios.append(self)
