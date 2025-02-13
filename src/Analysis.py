import numpy as np
import sympy as sp

# Last update: 2025 02 09

class Analysis:
    
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

            for carga in bar.lista_cargas:

                bar.vetor_esforcos[0] -= carga.qx * carga.length / 2
                bar.vetor_esforcos[1] -= carga.qy * carga.length / 2
                bar.vetor_esforcos[2] -= (carga.qy * carga.lx ** 2 / 12 + carga.qx * carga.ly ** 2 / 12)

                bar.vetor_esforcos[3] -= carga.qx * carga.length / 2
                bar.vetor_esforcos[4] -= carga.qy * carga.length / 2
                bar.vetor_esforcos[5] += (carga.qy * carga.lx ** 2 / 12 + carga.qx * carga.ly ** 2 / 12)

    def solver_viga(self):
        self.calcular_matriz_rigidez()
        self.calcular_vetor_deslocamentos()
        self.calcular_vetor_forcas()
        self.calcular_solucao()
        # self.set_displacements()
        # self.set_internal_forces()