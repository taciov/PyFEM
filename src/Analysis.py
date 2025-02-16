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

        self.obter_lista_graus()

        self.quant_nos = max(self.lista_nos_idx)
        self.quant_barras = len(self.lista_barras)
        self.k_global = sp.Matrix.zeros(len(self.lista_graus), len(self.lista_graus))

    def obter_lista_graus(self):
        self.lista_graus = []

        for barra in self.lista_barras:
            for node in barra.list_nodes:
                for grau in node.lista_graus:

                    if grau not in self.lista_graus:
                        self.lista_graus.append(grau)
    
    def calcular_matriz_rigidez(self):
        for barra in self.lista_barras:
            lista_graus_temp = []
            for node in barra.list_nodes:
                for grau in node.lista_graus:
                    lista_graus_temp.append(grau - 1)
            for i, grau1 in enumerate(lista_graus_temp):
                for j, grau2 in enumerate(lista_graus_temp):
                    self.k_global[grau1, grau2] += barra.ke[i + 1, j + 1]

    def calcular_vetor_forcas(self):

        self.vetor_forcas = np.zeros(len(self.lista_graus))

        for idx_node, node in enumerate(self.lista_nos):
            for idx_forces, forces in enumerate(node.forces_vector):
                self.vetor_forcas[len(node.forces_vector) * idx_node + idx_forces] = forces

    def calcular_vetor_deslocamentos(self):

        self.vetor_deslocamentos = np.zeros(len(self.lista_graus))

        for idx_node, node in enumerate(self.lista_nos):
            for idx_displacement, displacement in enumerate(node.displacement_vector):
                self.vetor_deslocamentos[len(node.displacement_vector)  * idx_node + idx_displacement] = displacement

    def calcular_solucao(self):
        list_positions = []
        for idx, u in enumerate(self.vetor_deslocamentos):
            if np.isnan(u) == True:
                list_positions.append(idx)
        tam = len(list_positions)
        self.k_shorted = np.zeros(shape=(tam, tam))
        
        for idx1, pos1 in enumerate(list_positions):
            for idx2, pos2 in enumerate(list_positions):
                self.k_shorted[idx1, idx2] = self.k_global[pos1, pos2]

        self.f_shorted = []
        for idx, pos in enumerate(list_positions):
            self.f_shorted.append(self.vetor_forcas[pos])
        
        # print(self.f_shorted)

        self.d_shorted = np.dot(np.linalg.inv(self.k_shorted), self.f_shorted)

        counter_temp = 0
        for idx, value in enumerate(self.vetor_deslocamentos):
            if np.isnan(value) == True:
                self.vetor_deslocamentos[idx] = self.d_shorted[counter_temp]
                counter_temp += 1

    def set_displacements(self):

        for node in self.lista_nos:
            for idx, grau in enumerate(node.lista_graus):
                node.displacement_vector[idx] = self.vetor_deslocamentos[grau - 1]      

        for bar in self.lista_barras:
            node1, node2 = bar.list_nodes
            d_global = np.hstack((np.array(node1.displacement_vector), np.array(node2.displacement_vector)))
            # print(d_global)
            vetor_deslocamentos = np.dot(bar.T, d_global)
            # print(vetor_deslocamentos)

            setattr(bar, 'vetor_deslocamentos', vetor_deslocamentos)
   
    def set_internal_forces(self):
        for bar in self.lista_barras:
            bar.vetor_esforcos = np.dot(bar.ke_, bar.vetor_deslocamentos)

            # for carga in bar.lista_cargas:

            #     bar.vetor_esforcos[0] -= carga.qx * carga.length / 2
            #     bar.vetor_esforcos[1] -= carga.qy * carga.length / 2
            #     bar.vetor_esforcos[2] -= (carga.qy * carga.lx ** 2 / 12 + carga.qx * carga.ly ** 2 / 12)

            #     bar.vetor_esforcos[3] -= carga.qx * carga.length / 2
            #     bar.vetor_esforcos[4] -= carga.qy * carga.length / 2
            #     bar.vetor_esforcos[5] += (carga.qy * carga.lx ** 2 / 12 + carga.qx * carga.ly ** 2 / 12)

    def solver(self):
        self.calcular_matriz_rigidez()
        self.calcular_vetor_deslocamentos()
        self.calcular_vetor_forcas()
        self.calcular_solucao()
        self.set_displacements()
        self.set_internal_forces()