import numpy as np
import sympy as sp
import matplotlib.pyplot as plt

# Last update: 2024 09 01

class Node:
    def __init__(self, x, y, indice):
        self.indice = indice
        self.lista_graus = [3 * indice - 2, 3 * indice - 1, 3 * indice]
        self.x = x
        self.y = y

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

    def substituir_coordenadas(self, x, y):
        self.x = x
        self.y = y

class Bar:   
    def __init__(self,  E, A, I, *args, **kwargs):
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

            # lista_graus = bar.lista_graus
            # node1, node2 = bar.list_nodes

            # node1.ex = 

    def solver_viga(self):
        self.calcular_matriz_rigidez()
        self.calcular_vetor_deslocamentos()
        self.calcular_vetor_forcas()
        self.calcular_solucao()
        self.set_displacements()
        self.set_internal_forces()

    def plot_displacement(self):
        for bar in self.lista_barras:
            x0 = [(node.x) for node in bar.list_nodes]
            y0 = [(node.y) * 1e3 for node in bar.list_nodes]
            x = [(node.x + node.ux) for node in bar.list_nodes]
            y = [(node.y + node.uy) * 1e3 for node in bar.list_nodes]
            plt.plot(x0, y0, color = 'blue', lw = 1)
            plt.plot(x, y, color = 'red', lw = 1, ls = '--')

        plt.title('Deformação da viga')
        plt.xlabel('Comprimento (m)')
        plt.ylabel('Deformação (mm)')
        # plt.ylim(bottom = 10 * np.min(array_uy), top = 10 * abs(np.min(array_uy)))
        plt.show()
    
    def plot_axial_force(self):
        for bar in self.lista_barras:
            x0 = [(node.x) for node in bar.list_nodes]
            y0 = [(node.y) * 1e3 for node in bar.list_nodes]
            ex = [- bar.vetor_esforcos[0] * 1e-3, bar.vetor_esforcos[3] * 1e-3]

            plt.plot(x0, y0, color = 'blue', lw = 1)
            plt.plot(x0, ex, color = 'red', lw = 1, ls = '--')
        
        plt.title('Diagrama de Esforço Normal')
        plt.xlabel('Comprimento (m)')
        plt.ylabel('Esforço Normal (kN)')
        # plt.ylim(bottom = 10 * np.min(array_uy), top = 10 * abs(np.min(array_uy)))
        plt.show()
    
    def plot_shear_force(self):
        for bar in self.lista_barras:
            x0 = [(node.x) for node in bar.list_nodes]
            y0 = [(node.y) * 1e3 for node in bar.list_nodes]
            ey = [bar.vetor_esforcos[1] * 1e-3, - bar.vetor_esforcos[4] * 1e-3]

            plt.plot(x0, y0, color = 'blue', lw = 1)
            plt.plot(x0, ey, color = 'red', lw = 1, ls = '--')
        
        plt.title('Diagrama de Esforço Cortante')
        plt.xlabel('Comprimento (m)')
        plt.ylabel('Esforço Cortante (kN)')
        # plt.ylim(bottom = 10 * np.min(array_uy), top = 10 * abs(np.min(array_uy)))
        plt.show()

    def plot_bending_moment(self):
        for bar in self.lista_barras:
            x0 = [(node.x) for node in bar.list_nodes]
            y0 = [(node.y) * 1e3 for node in bar.list_nodes]
            mf = [- bar.vetor_esforcos[2] * 1e-3, bar.vetor_esforcos[5] * 1e-3]

            plt.plot(x0, y0, color = 'blue', lw = 1)
            plt.plot(x0, mf, color = 'red', lw = 1, ls = '--')
        
        plt.title('Diagrama de Momento Fletor')
        plt.xlabel('Comprimento (m)')
        plt.ylabel('Momento Fletor (kNm)')
        # plt.ylim(bottom = 10 * np.min(array_uy), top = 10 * abs(np.min(array_uy)))
        plt.show()

    def plotar_momento_fletor(self):
        array_x = np.array([float(node.x) for node in self.lista_nos])
        array_mf = np.array([float(node.mf * 1e-3) for node in self.lista_nos])
        plt.plot(array_x, array_mf)
        plt.fill_between(array_x, array_mf, where=(array_mf >= 0), color = 'skyblue', interpolate= True)
        plt.fill_between(array_x, array_mf, where=(array_mf < 0), color = 'lightcoral', interpolate= True)
        plt.title('Momento Fletor')
        plt.xlabel('Comprimento (m)')
        plt.ylabel('Momento Fletor (kNm)')
        plt.grid()
        # plt.ylim(bottom = 10 * np.min(array_uy), top = 10 * abs(np.min(array_uy)))
        plt.show()

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

# bar1 = Bar(200e9, 8e-4, 1.067e-7, node1, node2)

# bar2 = Bar(200e9, 8e-4, 1.067e-7, node2, node3)

# bar3 = Bar(200e9, 8e-4, 1.067e-7, node3, node4)

# bar4 = Bar(200e9, 8e-4, 1.067e-7, node4, node5)

# beam1 = Beam(bar1, bar2, bar3, bar4)
# beam1.solver_viga()
# beam1.plot_displacement()
# beam1.plot_axial_force()
# beam1.plot_shear_force()
# beam1.plot_bending_moment()

