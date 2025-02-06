from src import Node as nd
from src import Apoio as ap
from src import Bar as bar
from src import MEFVigas as vg
from src import CargaPontual as cp
from src import CargaDistribuida as cd

class Modelo:

    def __init__(self):

        self.lista_nodes = []
        self.lista_apoios = []
        self.lista_barras = []
        self.lista_cargas = []

    def criar_node(self, x, y):
        node_temp = nd.Node(x, y)
        self.lista_nodes.append(node_temp)
    
    def identif_node(self, x, y):
        for idx, iter_node in enumerate(self.lista_nodes):
            if iter_node.x == x and iter_node.y == y:
                ident_node = iter_node
        
        return ident_node

    def criar_apoio(self, gl, node = None, ** kwargs):

        if 'x' and 'y' in kwargs:

            x = float(kwargs['x'])
            y = float(kwargs['y'])

            node = self.identif_node(x, y)
        
        apoio_temp = ap.Apoio(gl, node, ** kwargs)
        self.lista_apoios.append(apoio_temp)
        
    def criar_barra(self, E, A, I, node1, node2):
        barra_temp = bar.Barra(E, A, I, node1, node2)
        self.lista_barras.append(barra_temp)
        
    def criar_barras(self, E, A, I):
        for idx in range(len(self.lista_nodes) - 1):
            self.criar_barra(E, A, I, self.lista_nodes[idx], self.lista_nodes[idx + 1])
    
    def aplicar_carga_pontual(self, fx, fy, mt, node = None, ** kwargs):

        if 'x' and 'y' in kwargs:
            x = kwargs['x']
            y = kwargs['y']

            node_temp = self.identif_node(x, y)

        else:
            node_temp = node
        
        carga_temp = cp.CargaPontual(fx, fy, mt, node_temp)
        self.lista_cargas.append(carga_temp)

    def aplicar_carga_distribuida(self, qx, qy, barra = None):
        carga_temp = cd.CargaUniforme(qx, qy, barra)
        self.lista_cargas.append(carga_temp)
    
    ## CRIAR FUNCAO IDENT_BARRA PARA QUE EU CONSIGA SELECINAR A BARRA A PARTIR DE [X1, Y1], [X2, Y2]

    def criar_modelo(self):
        self.viga = vg.Beam(lista_barras = self.lista_barras)

    def processar_modelo(self):
        self.viga.solver_viga()