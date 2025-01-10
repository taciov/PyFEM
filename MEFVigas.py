import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import pandas as pd

# Last update: 2025 01 09

class Node:

    list_nodes = []

    def __init__(self, x, y):

        Node.list_nodes.append(self)
        self.indice = len(Node.list_nodes)
        self.lista_graus = [3 * self.indice - 2, 3 * self.indice - 1, 3 * self.indice]
        self.x = x
        self.y = y

        self.set_force()
        self.set_displacement()

    def set_force(self, **kwargs):
        if 'fx' in kwargs:
            self.fx = float(kwargs['fx'])
        else:
            self.fx = 0
        if 'fy' in kwargs:
            self.fy = float(kwargs['fy'])
        else:
            self.fy = 0
        if 'mz' in kwargs:
            self.mz = float(kwargs['mz'])
        else:
            self.mz = 0

    def set_displacement(self, **kwargs):
        if 'ux' in kwargs:
            self.ux = float(kwargs['ux'])
        else:
            self.ux = np.nan
        if 'uy' in kwargs:
            self.uy = float(kwargs['uy'])
        else:
            self.uy = np.nan
        if 'ang' in kwargs:
            self.ang = float(kwargs['ang'])
        else:
            self.ang = np.nan
    
    @classmethod
    def clear_list_nodes(cls):
        cls.list_nodes = []

class Bar:

    list_bars = []

    def __init__(self,  E, A, I, *args, **kwargs):

        Bar.list_bars.append(self)
        self.list_nodes = [node for node in args]
        L, self.theta = self.definir_geometria()

        self.ke_ = sp.Matrix([[E * A / L, 0, 0, -E * A / L, 0, 0],
                 [0, 12 * E * I / (L **3), 6 * E * I / (L ** 2), 0, -12 * E * I / (L **3), 6 * E * I / (L ** 2)],
                 [0, 6 * E * I / (L ** 2), 4 * E * I / L, 0, -6 * E * I / (L ** 2), 2 * E * I / L],
                 [-E * A / L, 0, 0, E * A / L, 0, 0],
                 [0, -12 * E * I / (L **3), -6 * E * I / (L ** 2), 0, 12 * E * I / (L **3), -6 * E * I / (L ** 2)],
                 [0, 6 * E * I / (L ** 2), 2 * E * I / L, 0, -6 * E * I / (L ** 2), 4 * E * I / L]
                 ])
        c = sp.cos(self.theta)
        s = sp.sin(self.theta)
        self.T = sp.Matrix([[c, s, 0, 0, 0, 0,],
                        [-s, c, 0, 0, 0, 0,],
                        [0, 0, 1, 0, 0, 0],
                        [0, 0, 0, c, s, 0],
                        [0, 0, 0, -s, c, 0],
                        [0, 0, 0, 0, 0, 1]
        ])
        self.A, self.E, self.L, self.I = A, E, L, I
        self.ke = self.T.T * self.ke_ * self.T

        self.get_forces_vector()
        self.atribuir_graus()

    def get_forces_vector(self):
        node1, node2 = self.list_nodes
        self.f = np.array([node1.fx, node1.fy, node1.mz, node2.fx, node2.fy, node2.mz])    

    def definir_geometria(self):
        node1, node2 = self.list_nodes
        x1, y1, x2, y2 = node1.x, node1.y, node2.x, node2.y
        length = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        if ((x2 - x1) == 0) and ((y2 - y1) > 0):
            theta = np.pi / 2
        elif ((x2 - x1) == 0) and ((y2 - y1) < 0):
            theta = 3 * np.pi / 2
        elif ((y2 - y1) == 0) and ((x2 - x1) > 0):
            theta = 0
        elif ((y2 - y1) == 0) and ((x2 - x1) < 0):
            theta = np.pi
        else:
            theta = np.arctan((y2 - y1) / (x2 - x1))
        
        return length, theta

    def atribuir_nos(self, primeiro_no, segundo_no):
        self.list_nodes = [primeiro_no, segundo_no]

    def atribuir_graus(self):
        self.lista_graus = []
        for node in self.list_nodes:
            for grau in node.lista_graus:
                self.lista_graus.append(grau)
        self.ke = self.ke.row_insert(0, sp.Matrix([self.lista_graus]))
        lista_graus_temp = self.lista_graus.copy()
        lista_graus_temp.append(0)
        self.ke = self.ke.col_insert(0, sp.Matrix(sorted(lista_graus_temp)))
    
    @classmethod
    def clear_list_bars(cls):
        cls.list_bars = []

class Beam:
    def __init__(self, *args, **kwargs):
        if 'lista_barras' in kwargs:
            self.lista_barras = kwargs['lista_barras']
        else:
            self.lista_barras = [barra for barra in args]
        self.lista_nos_idx = []
        self.lista_nos = []
        for barra in self.lista_barras:
            if barra.list_nodes[0] not in self.lista_nos:
                self.lista_nos.append(barra.list_nodes[0])
            if barra.list_nodes[1] not in self.lista_nos:
                self.lista_nos.append(barra.list_nodes[1])

        for barra in self.lista_barras:
            if barra.list_nodes[0].indice not in self.lista_nos_idx:
                self.lista_nos_idx.append(barra.list_nodes[0].indice)
            if barra.list_nodes[1].indice not in self.lista_nos_idx:
                self.lista_nos_idx.append(barra.list_nodes[1].indice)
        self.quant_nos = max(self.lista_nos_idx)
        self.quant_barras = len(self.lista_barras)
        self.k_global = sp.Matrix.zeros(3 * self.quant_nos, 3 * self.quant_nos)
    
    def calcular_matriz_rigidez(self):
        for barra in self.lista_barras:
            lista_graus_temp = []
            for node in barra.list_nodes:
                for grau in node.lista_graus:
                    lista_graus_temp.append(grau - 1)
            for i, grau1 in enumerate(lista_graus_temp):
                for j, grau2 in enumerate(lista_graus_temp):
                    self.k_global[grau1, grau2] += barra.ke[i + 1, j + 1]
    
    def calcular_vetor_deslocamentos(self):
        for indice, node in enumerate(self.lista_nos):
            if indice == 0:
                self.vetor_deslocamentos = np.array([[node.ux]])
                self.vetor_deslocamentos = np.vstack((self.vetor_deslocamentos, np.array([[node.uy]])))
                self.vetor_deslocamentos = np.vstack((self.vetor_deslocamentos, np.array([[node.ang]])))
            else:
                self.vetor_deslocamentos = np.vstack((self.vetor_deslocamentos, np.array([[node.ux]])))
                self.vetor_deslocamentos = np.vstack((self.vetor_deslocamentos, np.array([[node.uy]])))
                self.vetor_deslocamentos = np.vstack((self.vetor_deslocamentos, np.array([[node.ang]])))
        self.vetor_deslocamentos = sp.Matrix(self.vetor_deslocamentos)
    
    def calcular_vetor_forcas(self):
        for indice, node in enumerate(self.lista_nos):
            if indice == 0:
                self.vetor_forcas = np.array([[node.fx]])
                self.vetor_forcas = np.vstack((self.vetor_forcas, np.array([[node.fy]])))
                self.vetor_forcas = np.vstack((self.vetor_forcas, np.array([[node.mz]])))
            else:
                self.vetor_forcas = np.vstack((self.vetor_forcas, np.array([[node.fx]])))
                self.vetor_forcas = np.vstack((self.vetor_forcas, np.array([[node.fy]])))
                self.vetor_forcas = np.vstack((self.vetor_forcas, np.array([[node.mz]])))
        self.vetor_forcas = sp.Matrix(self.vetor_forcas)
    
    def calcular_solucao(self):
        list_positions = []
        for idx, u in enumerate(self.vetor_deslocamentos):
            if u == np.nan or u == sp.nan:
                list_positions.append(idx)
        tam = len(list_positions)
        self.k_shorted = np.zeros(shape=(tam, tam))
        
        for idx1, pos1 in enumerate(list_positions):
            for idx2, pos2 in enumerate(list_positions):
                self.k_shorted[idx1, idx2] = self.k_global[pos1, pos2]

        f_shorted = []
        for idx, pos in enumerate(list_positions):
            f_shorted.append(self.vetor_forcas[pos])
        
        d_shorted = np.dot(np.linalg.inv(self.k_shorted), f_shorted)

        counter_temp = 0
        for idx, value in enumerate(self.vetor_deslocamentos):
            if value == np.nan or value == sp.nan:
                self.vetor_deslocamentos[idx] = d_shorted[counter_temp]
                counter_temp += 1

    def set_displacements(self):
        for bar in self.lista_barras:
            lista_graus = bar.lista_graus
            node1, node2 = bar.list_nodes

            node1.ux = self.vetor_deslocamentos[lista_graus[0] - 1]
            node1.uy = self.vetor_deslocamentos[lista_graus[1] - 1]
            node1.ang = self.vetor_deslocamentos[lista_graus[2] - 1]

            node2.ux = self.vetor_deslocamentos[lista_graus[3] - 1]
            node2.uy = self.vetor_deslocamentos[lista_graus[4] - 1]
            node2.ang = self.vetor_deslocamentos[lista_graus[5] - 1]
    
        for bar in self.lista_barras:
            node1, node2 = bar.list_nodes
            d_global = np.array([node1.ux, node1.uy, node1.ang,
                                 node2.ux, node2.uy, node2.ang])
            
            bar.vetor_deslocamentos = np.dot(bar.T, d_global)
    
    def set_internal_forces(self):
        for bar in self.lista_barras:
            bar.vetor_esforcos = np.dot(bar.ke_, bar.vetor_deslocamentos)

    def solver_viga(self):
        self.calcular_matriz_rigidez()
        self.calcular_vetor_deslocamentos()
        self.calcular_vetor_forcas()
        self.calcular_solucao()
        self.set_displacements()
        self.set_internal_forces()

    def plot_displacement(self):
        # fig = go.Figure()
        for bar in self.lista_barras:
            scale = 1000
            x0 = [(node.x) for node in bar.list_nodes]
            y0 = [(node.y) for node in bar.list_nodes]
            x = [(node.x + node.ux * scale) for node in bar.list_nodes]
            y = [(node.y + node.uy * scale) for node in bar.list_nodes]
            plt.plot(x0, y0, color = 'blue', lw = 1)
            plt.plot(x, y, color = 'red', lw = 1, ls = '--')
            plt.axis('equal')

        plt.title('Deformação da viga')
        plt.xlabel('Comprimento (m)')
        plt.ylabel('Altura (m)')
        plt.show()

    def plot_displacement2(self):
        fig = go.Figure()
        scale = 1000

        for bar in self.lista_barras:
            x0 = np.array([float(node.x) for node in bar.list_nodes])
            y0 = np.array([float(node.y) for node in bar.list_nodes])

            x = np.array([float(node.x + node.ux * scale) for node in bar.list_nodes])
            y = np.array([float(node.y + node.uy * scale) for node in bar.list_nodes])

            fig.add_trace(go.Scatter(
                x=x0, y=y0,
                mode='lines',
                line=dict(color='blue', width=1)
            ))

            fig.add_trace(go.Scatter(
                x=x, y=y,
                mode='lines',
                line=dict(color='red', width=1, dash='dash')
            ))

        fig.update_layout(
            title='Deformação da viga',
            xaxis_title='Comprimento (m)',
            yaxis_title='Altura (m)',
            template='plotly_white',
            xaxis=dict(scaleanchor='y'),
            showlegend=False
        )

        fig.show()
    
    def plot_axial_force(self):
        for bar in self.lista_barras:
            scale = 0.005
            x0 = [(node.x) for node in bar.list_nodes]
            y0 = [(node.y)for node in bar.list_nodes]
            ex = [- bar.vetor_esforcos[0] * 1e-3, bar.vetor_esforcos[3] * 1e-3]
            exx = [xi + exi * (- np.sin(bar.theta)) * scale for xi, exi in zip(x0, ex)]
            exy = [yi + exi * (np.cos(bar.theta)) * scale for yi, exi in zip(y0, ex)]
            plt.plot(x0, y0, color = 'blue', lw = 1)
            plt.plot(exx, exy, color = 'red', lw = 1, ls = '--')
            plt.axis('equal')
        
        plt.title('Diagrama de Esforço Normal')
        plt.xlabel('Comprimento (m)')
        plt.ylabel('Altura (m)')
        plt.show()
    
    def plot_shear_force(self):
        for bar in self.lista_barras:
            scale = 0.01
            x0 = [(node.x) for node in bar.list_nodes]
            y0 = [(node.y) for node in bar.list_nodes]
            ey = [bar.vetor_esforcos[1] * 1e-3, - bar.vetor_esforcos[4] * 1e-3]
            eyx = [xi + eyi * (- np.sin(bar.theta)) * scale for xi, eyi in zip(x0, ey)]
            eyy = [yi + eyi * (np.cos(bar.theta)) * scale for yi, eyi in zip(y0, ey)]
            plt.plot(x0, y0, color = 'blue', lw = 1)
            plt.plot(eyx, eyy, color = 'red', lw = 1, ls = '--')
            plt.axis('equal')
        
        plt.title('Diagrama de Esforço Cortante')
        plt.xlabel('Comprimento (m)')
        plt.ylabel('Altura (m)')
        plt.show()

    def plot_bending_moment(self):
        for bar in self.lista_barras:
            scale = 0.05
            x0 = np.array([(node.x) for node in bar.list_nodes])
            y0 = np.array([(node.y) for node in bar.list_nodes])
            mf = np.array([- bar.vetor_esforcos[2] * 1e-3, bar.vetor_esforcos[5] * 1e-3])
            mfx = [xi + mfi * (np.sin(bar.theta)) * scale for xi, mfi in zip(x0, mf)]
            mfy = [yi + mfi * (- np.cos(bar.theta)) * scale for yi, mfi in zip(y0, mf)]
            plt.plot(x0, y0, color = 'blue', lw = 1)
            plt.plot(mfx, mfy, color = 'red', lw = 1, ls = '--')
            plt.axis('equal')
            # plt.gca().invert_yaxis()
        
        plt.title('Diagrama de Momento Fletor')
        plt.xlabel('Comprimento (m)')
        plt.ylabel('Altura (m)')
        plt.show()

    def export_data(self, **kwargs):
        if 'name' in kwargs:
            name = kwargs['name']
        else:
            name = 'file'
        for idx, bar in enumerate(self.lista_barras):
            if idx == 0:
                self.x0 = np.array([float(node.x) for node in bar.list_nodes])
                self.y0 = np.array([float(node.y) for node in bar.list_nodes])
                self.ux = np.array([float(node.ux) for node in bar.list_nodes])
                self.uy = np.array([float(node.uy) for node in bar.list_nodes])
                self.ex = [float(- bar.vetor_esforcos[0] * 1e-3), float(bar.vetor_esforcos[3] * 1e-3)]
                self.ey = [float(bar.vetor_esforcos[1] * 1e-3), float(- bar.vetor_esforcos[4] * 1e-3)]
                self.mf = np.array([float(- bar.vetor_esforcos[2] * 1e-3), float(bar.vetor_esforcos[5] * 1e-3)])
            
            else:
                self.x0 = np.hstack([self.x0, np.array([float(node.x) for node in bar.list_nodes])])
                self.y0 = np.hstack([self.y0, np.array([float(node.y) for node in bar.list_nodes])])
                self.ux = np.hstack([self.ux, np.array([float(node.ux) for node in bar.list_nodes])])
                self.uy = np.hstack([self.uy, np.array([float(node.uy) for node in bar.list_nodes])])
                self.ex = np.hstack([self.ex, [float(- bar.vetor_esforcos[0] * 1e-3), float(bar.vetor_esforcos[3] * 1e-3)]])
                self.ey = np.hstack([self.ey, [float(bar.vetor_esforcos[1] * 1e-3), float(- bar.vetor_esforcos[4] * 1e-3)]])
                self.mf = np.hstack([self.mf, np.array([float(- bar.vetor_esforcos[2] * 1e-3), float(bar.vetor_esforcos[5] * 1e-3)])])

        self.data = np.array([self.x0,
                              self.y0,
                              self.ux,
                              self.uy,
                              self.ex,
                              self.ey,
                              self.mf])
    
        self.dict_data = {'x' : self.x0.tolist(),
                          'y' : self.y0.tolist(),
                          'ux' : self.ux.tolist(),
                          'uy' : self.uy.tolist(),
                          'ex' : self.ex.tolist(),
                          'ey' : self.ey.tolist(),
                          'mf' : self.mf.tolist()}
        
        df_data = pd.DataFrame(self.dict_data)
        df_data.to_json(f'{name}.json', indent = 2)

## Exemplo

# node1 = Node(0, 0, 1)
# node1.set_force(fx = 0, fy = 0, mz = 0)
# node1.set_displacement(ux = 0, uy = 0)

# node2 = Node(0.25, 0, 2)
# node2.set_force(fx = 0, fy = -10e3 / 3, mz = 0)
# node2.set_displacement()

# node3 = Node(0.5, 0, 3)
# node3.set_force(fx = 10e3, fy = -10e3 / 3, mz = 0)
# node3.set_displacement()

# node4 = Node(0.75, 0, 4)
# node4.set_force(fx = 0, fy = -10e3 / 3, mz = 0)
# node4.set_displacement()

# node5 = Node(1, 0, 5)
# node5.set_force(fx = 0, fy = 0, mz = 0)
# node5.set_displacement(ux = 0, uy = 0)

# mod_elast = 200e9
# b = 0.2
# h = 0.4
# area = b * h
# inercia = b * h ** 3 / 12

# bar1 = Bar(mod_elast, area, inercia, node1, node2)

# bar2 = Bar(mod_elast, area, inercia, node2, node3)

# bar3 = Bar(mod_elast, area, inercia, node3, node4)

# bar4 = Bar(mod_elast, area, inercia, node4, node5)

# beam1 = Beam(bar1, bar2, bar3, bar4)
# beam1.solver_viga()
# beam1.plot_displacement()
# beam1.plot_axial_force()
# beam1.plot_shear_force()
# beam1.plot_bending_moment()