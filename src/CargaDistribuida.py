import numpy as np

class CargaUniforme:
    def __init__(self, qx, qy, qz, bar):

        self.type = 'uniforme'
        self.qx = qx
        self.qy = qy
        self.qz = qz

        node0 = bar.list_nodes[0]
        node1 = bar.list_nodes[1]

        self.x0 = node0.x
        self.y0 = node0.y
        self.z0 = node0.z
        self.x1 = node1.x
        self.y1 = node1.y
        self.z1 = node1.z
        
        self.length = bar.L
        self.theta = bar.theta

        self.lx = self.length * np.cos(self.theta)
        self.ly = self.length * np.sin(self.theta)

        node0.fx += self.qx * self.length / 2
        node0.fy += self.qy * self.length / 2
        node0.fz += self.qz * self.length / 2

        node0.mz += self.qy * self.lx ** 2 / 12 + self.qx * self.ly ** 2 / 12

        node1.fx += self.qx * self.length / 2
        node1.fy += self.qy * self.length / 2
        node1.mz -= self.qy * self.lx ** 2 / 12 + self.qx * self.ly ** 2 / 12
        
