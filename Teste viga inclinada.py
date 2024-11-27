## Teste viga inclinada

from MEFVigas import Node, Bar, Beam
import numpy as np
import matplotlib.pyplot as plt

## Definindo as coordenadas dos nos

x = np.linspace(0, 4, 5)
y = np.array([0, 0.5, 1, 0.5, 0])
# plt.plot(x, y)

node1 = Node(x[0], y[0], 1)
node1.set_force(fx = 0, fy = 0, mz = 0)
node1.set_displacement(ux = 0, uy = 0)

node2 = Node(x[1], y[1], 2)
node2.set_force(fx = 0, fy = -10e3 / 3, mz = 0)
node2.set_displacement()

node3 = Node(x[2], y[2], 3)
node3.set_force(fx = 10e3, fy = -10e3 / 3, mz = 0)
node3.set_displacement()

node4 = Node(x[3], y[3], 4)
node4.set_force(fx = 0, fy = -10e3 / 3, mz = 0)
node4.set_displacement()

node5 = Node(x[4], y[4], 5)
node5.set_force(fx = 0, fy = 0, mz = 0)
node5.set_displacement(ux = 0, uy = 0)

mod_elast = 200e9
b = 0.2
h = 0.4
area = b * h
inercia = b * h ** 3 / 12

bar1 = Bar(mod_elast, area, inercia, node1, node2)

bar2 = Bar(mod_elast, area, inercia, node2, node3)

bar3 = Bar(mod_elast, area, inercia, node3, node4)

bar4 = Bar(mod_elast, area, inercia, node4, node5)

beam1 = Beam(bar1, bar2, bar3, bar4)
beam1.solver_viga()
beam1.plot_displacement()
beam1.plot_axial_force()
beam1.plot_shear_force()
beam1.plot_bending_moment()

