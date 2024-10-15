from MEFVigas import Nos, Barra, Viga
from MEFCargas import CargaPontual, CargaUniforme, Apoio
# from VigaFlexao import VigaRetangular
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt

## Propriedades da viga

numero_nos = 31
length = 6
length_unit = length / (numero_nos - 1)
base = 20 / 100
altura = 50 / 100
area = base * altura
momento_inercia = (base * altura ** 3) / 12
modulo_elast = 30e9

## Criando os apoios

apoio1 = Apoio([0, 0], 0, 0, 1)
apoio2 = Apoio([2, 0], 0, 0, 1)
apoio3 = Apoio([4, 0], 0, 0, 1)
apoio4 = Apoio([6, 0], 0, 0, 1)
# apoio4 = Apoio([4, 0], 0, 0, 1)

lista_apoios = [apoio1, apoio2, apoio3, apoio4]

## Criando a carga distribuida

carga_dist = CargaUniforme(0, -68e3, 0, x1 = 0, y1 = 0, x2 = 6, y2 = 0)
lista_cargas = [carga_dist]

## Criando os nós

lista_nos = [Nos(x) for x in range(1, numero_nos + 1)]

## Atribuindo as coordenadas dos nos:

for idx, node in enumerate(lista_nos):
    x = length * (idx) / (len(lista_nos) - 1)
    y = 0
    node.substituir_coordenadas(x, y)

## Atribuindo propriedades dos apoios:

lista_nos_aux = []
lista_apoios_aux = []
for node in lista_nos:
    node.atribuir_esforcos()
    for apoio in lista_apoios:
        if node not in lista_nos_aux and apoio not in lista_apoios_aux:
            if float(apoio.x) == float(node.x) and float(apoio.y) == float(node.y):
                setattr(apoio, 'node', node)
                if apoio.fx == 1 and apoio.fy == 1 and apoio.mt == 1:
                    node.atribuir_forcas(fx = 0, fy = 0, mt = 0)
                    node.atribuir_deslocamentos()
                
                elif apoio.fx == 0 and apoio.fy == 1 and apoio.mt == 1:
                    node.atribuir_forcas(fy = 0, mt = 0)
                    node.atribuir_deslocamentos(ux = 0)
                
                elif apoio.fx == 1 and apoio.fy == 0 and apoio.mt == 1:
                    node.atribuir_forcas(fx = 0, mt = 0)
                    node.atribuir_deslocamentos(uy = 0)
                
                elif apoio.fx == 1 and apoio.fy == 1 and apoio.mt == 0:
                    node.atribuir_forcas(fx = 0, fy = 0)
                    node.atribuir_deslocamentos(ang = 0)
                
                elif apoio.fx == 1 and apoio.fy == 0 and apoio.mt == 0:
                    node.atribuir_forcas(fx = 0)
                    node.atribuir_deslocamentos(uy = 0, ang = 0)
                
                elif apoio.fx == 0 and apoio.fy == 1 and apoio.mt == 0:
                    node.atribuir_forcas(fy = 0)
                    node.atribuir_deslocamentos(ux = 0, ang = 0)
                
                elif apoio.fx == 0 and apoio.fy == 0 and apoio.mt == 1:
                    node.atribuir_forcas(mt = 0)
                    node.atribuir_deslocamentos(ux = 0, uy = 0)
                
                else:
                    node.atribuir_forcas()
                    node.atribuir_deslocamentos(ux = 0, uy = 0, ang = 0)
                
                lista_nos_aux.append(node)
                lista_apoios_aux.append(apoio)
                    
            else:
                node.atribuir_forcas(fx = 0, fy = 0, mt = 0)
                node.atribuir_deslocamentos()

## Atribuindo as propriedades das cargas

for carga in lista_cargas:
    carga.definir_nos(lista_nos)
    qux = carga.qx * carga.length / len(carga.lista_nos)
    quy = carga.qy * carga.length / len(carga.lista_nos)
    for node in carga.lista_nos:
        # setattr(node, 'fx', qux)
        # setattr(node, 'fy', quy)
        setattr(node, 'fx', node.fx + qux)
        setattr(node, 'fy', node.fy + quy)

## Criando as barras

lista_barras = [Barra() for x in range(numero_nos - 1)]

for indice, barra in enumerate(lista_barras):
    barra.atribuir_nos(lista_nos[indice], lista_nos[indice + 1])
    barra.atribuir_graus()
    barra.atribuir_valores(area, modulo_elast, momento_inercia)
    

## Criando a viga

beam = Viga(lista_barras = lista_barras)
beam.solver_viga()

beam.plotar_deslocamentos()
beam.plotar_esforco_cortante()
beam.plotar_momento_fletor()


## VERIFICAR A NECESSIDADE DE DESCREVER A FORÇA NOS APOIOS COMO SENDO A CARGA + A INCOGNITA DA REAÇÃO