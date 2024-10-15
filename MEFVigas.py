import numpy as np
import sympy as sp
import matplotlib.pyplot as plt

# Last update: 2024 09 01

class Nos:
    def __init__(self, indice):
        self.indice = indice
        self.lista_graus = [3 * indice - 2, 3 * indice - 1, 3 * indice]
        self.fx, self.fy, self.mt = sp.symbols([f'fx{self.indice}', f'fy{self.indice}', f'mt{self.indice}'])
        self.ux, self.uy, self.ang = sp.symbols([f'ux{self.indice}', f'uy{self.indice}', f'ang{self.indice}'])

    def atribuir_forcas(self, **kwargs):
        if 'fx' in kwargs:
            self.fx = self.fx.subs(self.fx, kwargs['fx'])
        if 'fy' in kwargs:
            self.fy = self.fy.subs(self.fy, kwargs['fy'])
        if 'mt' in kwargs:
            self.mt = self.mt.subs(self.mt, kwargs['mt'])

    def atribuir_deslocamentos(self, **kwargs):
        if 'ux' in kwargs:
            self.ux = self.ux.subs(self.ux, kwargs['ux'])
        if 'uy' in kwargs:
            self.uy = self.uy.subs(self.uy, kwargs['uy'])
        if 'ang' in kwargs:
            self.ang = self.ang.subs(self.ang, kwargs['ang'])
    
    def atribuir_esforcos(self, **kwargs):
        self.ex = 0
        self.ey = 0
        self.mf = 0
        if 'ex' in kwargs:
            self.ex = kwargs['ex']
        if 'ey' in kwargs:
            self.ey = kwargs['ey']
        if 'mf' in kwargs:
            self.mf = kwargs['mf']

    def substituir_coordenadas(self, x, y):
        self.x = x
        self.y = y

class Barra:   
    def __init__(self, *args, **kwargs):
        self.barra_nos = [node for node in args]
        A, E, L, I = sp.symbols(['A', 'E', 'L', 'I'])
        self.theta = sp.symbols('theta')
        ke_ = sp.Matrix([[E * A / L, 0, 0, -E * A / L, 0, 0],
                 [0, 12 * E * I / (L **3), 6 * E * I / (L ** 2), 0, -12 * E * I / (L **3), 6 * E * I / (L ** 2)],
                 [0, 6 * E * I / (L ** 2), 4 * E * I / L, 0, -6 * E * I / (L ** 2), 2 * E * I / L],
                 [-E * A / L, 0, 0, E * A / L, 0, 0],
                 [0, -12 * E * I / (L **3), -6 * E * I / (L ** 2), 0, 12 * E * I / (L **3), -6 * E * I / (L ** 2)],
                 [0, 6 * E * I / (L ** 2), 2 * E * I / L, 0, -6 * E * I / (L ** 2), 4 * E * I / L]
                 ])
        c = sp.cos(self.theta)
        s = sp.sin(self.theta)
        T = sp.Matrix([[c, -s, 0, 0, 0, 0,],
                        [s, c, 0, 0, 0, 0,],
                        [0, 0, 1, 0, 0, 0],
                        [0, 0, 0, c, -s, 0],
                        [0, 0, 0, s, c, 0],
                        [0, 0, 0, 0, 0, 1]
        ]).T
        self.A, self.E, self.L, self.I = A, E, L, I
        self.ke = T.T*ke_*T
   
    def atribuir_valores(self, area, elasticity, inertia):
        length, theta = self.definir_geometria()
        self.ke = self.ke.subs([(self.A, area),
                                (self.E, elasticity),
                                (self.L, length),
                                (self.I, inertia),
                                (self.theta, theta)])
        self.A = self.A.subs(self.A, area)
        self.E = self.E.subs(self.E, elasticity)
        self.I = self.I.subs(self.I, inertia)       

    def definir_geometria(self):
        node1, node2 = self.barra_nos
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
        self.barra_nos = [primeiro_no, segundo_no]

    def atribuir_graus(self):
        lista_graus_temp = []
        for node in self.barra_nos:
            for grau in node.lista_graus:
                lista_graus_temp.append(grau)
        self.ke = self.ke.row_insert(0, sp.Matrix([lista_graus_temp]))
        lista_graus_temp.append(0)
        self.ke = self.ke.col_insert(0, sp.Matrix(sorted(lista_graus_temp)))

class Viga:
    def __init__(self, *args, **kwargs):
        if 'lista_barras' in kwargs:
            self.lista_barras = kwargs['lista_barras']
        else:
            self.lista_barras = [barra for barra in args]
        self.lista_nos_idx = []
        self.lista_nos = []
        for barra in self.lista_barras:
            if barra.barra_nos[0] not in self.lista_nos:
                self.lista_nos.append(barra.barra_nos[0])
            if barra.barra_nos[1] not in self.lista_nos:
                self.lista_nos.append(barra.barra_nos[1])

        for barra in self.lista_barras:
            if barra.barra_nos[0].indice not in self.lista_nos_idx:
                self.lista_nos_idx.append(barra.barra_nos[0].indice)
            if barra.barra_nos[1].indice not in self.lista_nos_idx:
                self.lista_nos_idx.append(barra.barra_nos[1].indice)
        self.quant_nos = max(self.lista_nos_idx)
        self.quant_barras = len(self.lista_barras)
        self.k_global = sp.Matrix.zeros(3 * self.quant_nos, 3 * self.quant_nos)
    
    def calcular_matriz_rigidez(self):
        for barra in self.lista_barras:
            lista_graus_temp = []
            for node in barra.barra_nos:
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
                self.vetor_forcas = np.vstack((self.vetor_forcas, np.array([[node.mt]])))
            else:
                self.vetor_forcas = np.vstack((self.vetor_forcas, np.array([[node.fx]])))
                self.vetor_forcas = np.vstack((self.vetor_forcas, np.array([[node.fy]])))
                self.vetor_forcas = np.vstack((self.vetor_forcas, np.array([[node.mt]])))
        self.vetor_forcas = sp.Matrix(self.vetor_forcas)
    
    def calcular_solucao(self):
        # self.sistema_eq = self.k_global * self.vetor_deslocamentos -  self.vetor_forcas
        self.sistema_eq = np.dot(self.k_global, self.vetor_deslocamentos) -  self.vetor_forcas
        self.solucao = sp.solve(self.sistema_eq)

        ## Pesquisar alternativas ao sp.solve
    
    def atribuir_deslocamentos_calculados(self):
        for indice, node in enumerate(self.lista_nos):
            ux, uy, ang, fx, fy, mt = sp.symbols([f'ux{indice + 1}', f'uy{indice + 1}', f'ang{indice + 1}',
            f'fx{indice + 1}', f'fy{indice + 1}', f'mt{indice + 1}'])
            if ux in self.solucao.keys():
                setattr(self.lista_nos[indice], 'ux', self.solucao[ux])
            if uy in self.solucao.keys():
                setattr(self.lista_nos[indice], 'uy', self.solucao[uy])
            if ang in self.solucao.keys():
                setattr(self.lista_nos[indice], 'ang', self.solucao[ang])
            if fx in self.solucao.keys():
                setattr(self.lista_nos[indice], 'fx', self.solucao[fx])
            if fy in self.solucao.keys():
                setattr(self.lista_nos[indice], 'fy', self.solucao[fy])
            if mt in self.solucao.keys():
                setattr(self.lista_nos[indice], 'mt', self.solucao[mt])
    
    def atribuir_esforcos_internos(self):
        for barra in self.lista_barras:
            node1 = barra.barra_nos[0]
            node2 = barra.barra_nos[1]

            displacement_vector = np.array([node1.ux,
                                            node1.uy,
                                            node1.ang,
                                            node2.ux,
                                            node2.uy,
                                            node2.ang])
            
            barra_temp = np.zeros(shape=(6,6))
            for i in range(len(barra_temp[0,:])):
                for j in range(len(barra_temp[:, 0])):
                    barra_temp[i, j] = barra.ke[i + 1, j + 1]

            internal_forces_vector = np.dot(barra_temp, displacement_vector)
            
            setattr(node1, 'ex', internal_forces_vector[0])
            setattr(node1, 'ey', internal_forces_vector[1])
            setattr(node1, 'mf', internal_forces_vector[2])
            setattr(node2, 'ex', internal_forces_vector[3])
            setattr(node2, 'ey', internal_forces_vector[4])
            setattr(node2, 'mf', internal_forces_vector[5])

    def solver_viga(self):
        self.calcular_matriz_rigidez()
        self.calcular_vetor_deslocamentos()
        self.calcular_vetor_forcas()
        self.calcular_solucao()
        self.atribuir_deslocamentos_calculados()
        self.atribuir_esforcos_internos()

    def plotar_deslocamentos(self):
        lista_x = [node.x for node in self.lista_nos]
        lista_y = [node.y for node in self.lista_nos]
        lista_uy = []
        for indice, node in enumerate(self.lista_nos):
            lista_uy.append(vars(self.lista_nos[indice])['uy'] * 1e3)
        array_x = np.array(lista_x, dtype=float)
        array_uy = np.array(lista_uy, dtype=float)
        plt.plot(array_x, lista_y)
        plt.plot(lista_x, lista_uy)

        plt.title('Deformação da viga')
        plt.xlabel('Comprimento (m)')
        plt.ylabel('Deformação (mm)')
        plt.ylim(bottom = 10 * np.min(array_uy), top = 10 * abs(np.min(array_uy)))
        plt.show()
    
    def plotar_esforco_normal(self):
        array_x = np.array([float(node.x) for node in self.lista_nos])
        array_ex = np.array([float(node.ex * 1e-3) for node in self.lista_nos])
        plt.plot(array_x, array_ex)
        plt.fill_between(array_x, array_ex, where=(array_ex >= 0), color = 'skyblue', interpolate= True)
        plt.fill_between(array_x, array_ex, where=(array_ex < 0), color = 'lightcoral', interpolate= True)
        plt.title('Esforço Cortante')
        plt.xlabel('Comprimento (m)')
        plt.ylabel('Força (kN)')
        plt.grid()
        # plt.ylim(bottom = 10 * np.min(array_uy), top = 10 * abs(np.min(array_uy)))
        plt.show()

    def plotar_esforco_cortante(self):
        array_x = np.array([float(node.x) for node in self.lista_nos])
        array_ey = np.array([float(node.ey * 1e-3) for node in self.lista_nos])
        plt.plot(array_x, array_ey)
        plt.fill_between(array_x, array_ey, where=(array_ey >= 0), color = 'skyblue', interpolate= True)
        plt.fill_between(array_x, array_ey, where=(array_ey < 0), color = 'lightcoral', interpolate= True)
        plt.title('Esforço Cortante')
        plt.xlabel('Comprimento (m)')
        plt.ylabel('Força (kN)')
        plt.grid()
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