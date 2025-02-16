class CargaPontual:

    list_carga_pontual = []

    def __init__(self, fx, fy, fz, mx, my, mz, node):

        self.node = node
        self.type = 'pontual'

        self.fx = fx
        self.fy = fy
        self.fz = fz
        self.mx = mx
        self.my = my
        self.mz = mz

        self.x = node.x
        self.y = node.y
        self.z = node.z

        node.fx += self.fx
        node.fy += self.fy
        node.fz += self.fz

        node.mx += self.mx
        node.my += self.my
        node.mz += self.mz

        CargaPontual.list_carga_pontual.append(self)
        node.get_forces_vector()