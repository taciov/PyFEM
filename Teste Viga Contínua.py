## Viga Contínua

from MEFVigas import Node, Bar, Beam
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

## Propriedades do material

mod_elast = 25e9
b = 0.2
h = 0.4
area = b * h
inercia = b * h ** 3 / 12

## Propriedades gerais da viga:

q = -10e3
L = 5

## Definindo os nós:

n1 = 11

x0 = np.linspace(0, 5, n1)
y0 = np.zeros(shape=(len(x0)))

## Força em cada nó:

fu = q * L / (n1 - 2)

list_nodes = []
for idx, [x, y] in enumerate(zip(x0, y0)):
    node_temp = Node(x, y, idx + 1)

    if x not in [1, 4]:
        node_temp.set_force(fx = 0, fy = fu, mz = 0)
        node_temp.set_displacement()
    
    else:
        node_temp.set_force(fx = 0, fy = 0, mz = 0)
        node_temp.set_displacement(ux = 0, uy = 0)

    list_nodes.append(node_temp)

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
beam1.export_data(name = 'viga_cont_11')

## Definindo os nós:

n2 = 21

x0 = np.linspace(0, 5, n2)
y0 = np.zeros(shape=(len(x0)))

## Força em cada nó:

fu = q * L / (n2 - 2)

list_nodes = []
for idx, [x, y] in enumerate(zip(x0, y0)):
    node_temp = Node(x, y, idx + 1)

    if x not in [1, 4]:
        node_temp.set_force(fx = 0, fy = fu, mz = 0)
        node_temp.set_displacement()
    
    else:
        node_temp.set_force(fx = 0, fy = 0, mz = 0)
        node_temp.set_displacement(ux = 0, uy = 0)

    list_nodes.append(node_temp)

## Definindo as barras:

list_bars = []

for idx in range(len(list_nodes) - 1):
    bar_temp = Bar(mod_elast, area, inercia, list_nodes[idx], list_nodes[idx + 1])
    list_bars.append(bar_temp)

beam2 = Beam(lista_barras = list_bars)
beam2.solver_viga()
beam2.plot_displacement()
# beam2.plot_displacement2()
beam2.plot_axial_force()
beam2.plot_shear_force()
beam2.plot_bending_moment()
beam2.export_data(name = 'viga_cont_21')

## Definindo os nós:

n3 = 51

x0 = np.linspace(0, 5, n3)
y0 = np.zeros(shape=(len(x0)))

## Força em cada nó:

fu = q * L / (n3 - 2)

list_nodes = []
for idx, [x, y] in enumerate(zip(x0, y0)):
    node_temp = Node(x, y, idx + 1)

    if x not in [1, 4]:
        node_temp.set_force(fx = 0, fy = fu, mz = 0)
        node_temp.set_displacement()
    
    else:
        node_temp.set_force(fx = 0, fy = 0, mz = 0)
        node_temp.set_displacement(ux = 0, uy = 0)

    list_nodes.append(node_temp)

## Definindo as barras:

list_bars = []

for idx in range(len(list_nodes) - 1):
    bar_temp = Bar(mod_elast, area, inercia, list_nodes[idx], list_nodes[idx + 1])
    list_bars.append(bar_temp)

beam3 = Beam(lista_barras = list_bars)
beam3.solver_viga()
beam3.plot_displacement()
# beam3.plot_displacement2()
beam3.plot_axial_force()
beam3.plot_shear_force()
beam3.plot_bending_moment()
beam3.export_data(name = 'viga_cont_51')

## DataFrames dos resultados:

df_1 = pd.DataFrame(beam1.dict_data)
df_2 = pd.DataFrame(beam2.dict_data)
df_3 = pd.DataFrame(beam3.dict_data)

display(df_1.loc[(df_1['x'] == 1) | (df_1['x'] == 2.5) |  (df_1['x'] == 4)])
display(df_2.loc[(df_2['x'] == 1) | (df_2['x'] == 2.5) |  (df_2['x'] == 4)])
display(df_3.loc[(df_3['x'] == 1) | (df_3['x'] == 2.5) |  (df_3['x'] == 4)])