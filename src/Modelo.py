from src import Node as nd
from src import Apoio as ap
from src import Bar as bar
from src import MEFVigas as vg

class Modelo:

    lista_barras = []

    def __init__(self):
        pass

    def criar_node(self, x, y):
        nd.Node(x, y)

    def criar_apoio(self, gl, x, y, ** kwargs):
        ap.Apoio(gl, x, y, ** kwargs)
    
    def criar_barra(self, E, A, I, node1, node2):
        bar.Barra(E, A, I, node1, node2)
    
    def criar_barras(self, E, A, I):
        for idx in range(len(nd.Node.list_nodes) - 1):
            bar.Barra(E, A, I, nd.Node.list_nodes[idx], nd.Node.list_nodes[idx + 1])
    
    def criar_modelo(self):
        viga = vg.Beam(lista_barras = bar.Barra.list_bars)
        self.lista_barras.append(viga)