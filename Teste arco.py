## Teste arco

from MEFVigas import Node, Bar, Beam
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

x0 = np.array([0 + np.cos(theta) for theta in np.linspace(0, np.pi, 51)])
y0 = np.array([0 + np.sin(theta) for theta in np.linspace(0, np.pi, 51)])

plt.plot(x0, y0)
plt.axis('equal')

## Definindo os nós:

list_nodes = []
for idx, [x, y] in enumerate(zip(x0, y0)):
    node_temp = Node(x, y, idx + 1)

    if idx not in [0, len(x0) - 1]:
        node_temp.set_force(fx = 0, fy = -10e3 / 3, mz = 0)
        node_temp.set_displacement()
    
    else:
        node_temp.set_force(fx = 0, fy = 0, mz = 0)
        node_temp.set_displacement(ux = 0, uy = 0)

    list_nodes.append(node_temp)

## Propriedades do material

mod_elast = 200e9
b = 0.2
h = 0.4
area = b * h
inercia = b * h ** 3 / 12

## Definindo as barras:

list_bars = []

for idx in range(len(list_nodes) - 1):
    bar_temp = Bar(mod_elast, area, inercia, list_nodes[idx], list_nodes[idx + 1])
    list_bars.append(bar_temp)

beam1 = Beam(lista_barras = list_bars)
beam1.solver_viga()
beam1.plot_displacement()
# beam1.plot_displacement2()
beam1.plot_axial_force()
beam1.plot_shear_force()
beam1.plot_bending_moment()
beam1.export_data()