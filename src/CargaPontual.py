class CargaPontual:

    list_carga_pontual = []

    def __init__(self, fx, fy, mt, node):
        self.node = node
        self.type = 'pontual'
        self.fx = fx
        self.fy = fy
        self.mt = mt
        self.x = node.x
        self.y = node.y

        node.fx += self.fx
        node.fy += self.fy
        node.mt += self.mt

        CargaPontual.list_carga_pontual.append(self)