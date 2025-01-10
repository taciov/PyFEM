class CargaUniforme:
    def __init__(self, qx, qy, bar):
        self.type = 'uniforme'
        self.qx = qx
        self.qy = qy

        node0 = bar.list_nodes[0]
        node1 = bar.list_nodes[1]

        self.x0 = node0.x
        self.y0 = node0.y
        self.x1 = node1.x
        self.y1 = node1.y
        
        # self.length = ((self.x1 - self.x0) ** 2 + (self.y1 - self.y0) ** 2) ** (1 / 2)
        self.length = bar.L

        node0.fx += self.qx * self.length / 2
        node0.fy += self.qy * self.length / 2
        # node0.mz += self.qy * self.length ** 2 / 12

        node1.fx += self.qx * self.length / 2
        node1.fy += self.qy * self.length / 2
        # node1.mz -= self.qy * self.length ** 2 / 12
        
