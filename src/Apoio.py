from src import Node as nd

class Apoio:

    list_apoios = []

    def __init__(self, gl, node = None, ** kwargs):

        self.glx = gl[0]
        self.gly = gl[1]
        self.glz = gl[2]
            
        if 'x' and 'y' in kwargs:

            self.x = float(kwargs['x'])
            self.y = float(kwargs['y'])

            self.node = self.identif_node(self.x, self.y)

            # self.node = nd.Node(self.x, self.y)

        else:
            self.node = node

            self.x = self.node.x
            self.y = self.node.y

        if self.glx == 0:
            self.node.ux = 0
        
        if self.gly == 0:
            self.node.uy = 0

        if self.glz == 0:
            self.node.ang = 0
        
        self.indice = self.node.indice
        
        Apoio.list_apoios.append(self)
    
    def identif_node(self, x, y):
        for idx, iter_node in enumerate(nd.Node.list_nodes):
            if iter_node.x == x and iter_node.y == y:
                ident_node = iter_node
        
        return ident_node
