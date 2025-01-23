class CargaPontual:

    list_carga_pontual = []

    def __init__(self, fx, fy, mz, node):
        self.node = node
        self.type = 'pontual'
        self.fx = fx
        self.fy = fy
        self.mz = mz
        self.x = node.x
        self.y = node.y

        node.fx += self.fx
        node.fy += self.fy
        node.mz += self.mz

        CargaPontual.list_carga_pontual.append(self)