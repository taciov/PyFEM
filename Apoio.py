class Apoio:

    list_apoios = []

    def __init__(self, gl, node):
        self.x = node.x
        self.y = node.y
        self.indice = node.indice

        self.glx = gl[0]
        self.gly = gl[1]
        self.glz = gl[2]
        
        if self.glx == 0:
            node.ux = 0
        
        if self.gly == 0:
            node.uy = 0

        if self.glz == 0:
            node.ang = 0
        
        Apoio.list_apoios.append(self)
