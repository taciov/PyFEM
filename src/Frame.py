# from src import Node as nd

import sympy as sp
import numpy as np

class Frame:

    list_bars = []
    
    def __init__(self, A, J, Iy, Iz, E, G, *args):

        self.lista_cargas = []
        Frame.list_bars.append(self)
        self.list_nodes = [node for node in args]
        L, self.theta_x, self.theta_y, self.theta_z, self.rotate = self.definir_geometria()

        self.ke_ = sp.Matrix([
            [E*A*L**2 / L**3, 0, 0, 0, 0, 0, -E*A*L**2 / L**3, 0, 0, 0, 0, 0],
            [0, E*12*Iz / L**3, 0, 0, 0, E*6*L*Iz / L**3, 0, -E*12*Iz / L**3, 0, 0, 0, E*6*L*Iz / L**3],
            [0, 0, E*12*Iy / L**3, 0, -E*6*L*Iy / L**3, 0, 0, 0, -E*12*Iy / L**3, 0, -E*6*L*Iy / L**3, 0],
            [0, 0, 0, E*G*J*L**2 / (E*L**3), 0, 0, 0, 0, 0, -E*G*J*L**2 / (E*L**3), 0, 0],
            [0, 0, -E*6*L*Iy / L**3, 0, E*4*L**2*Iy / L**3, 0, 0, 0, E*6*L*Iy / L**3, 0, E*2*L**2*Iy / L**3, 0],
            [0, E*6*L*Iz / L**3, 0, 0, 0, E*4*L**2*Iz / L**3, 0, -E*6*L*Iz / L**3, 0, 0, 0, E*2*L**2*Iz / L**3],
            [-E*A*L**2 / L**3, 0, 0, 0, 0, 0, E*A*L**2 / L**3, 0, 0, 0, 0, 0],
            [0, -E*12*Iz / L**3, 0, 0, 0, -E*6*L*Iz / L**3, 0, E*12*Iz / L**3, 0, 0, 0, -E*6*L*Iz / L**3],
            [0, 0, -E*12*Iy / L**3, 0, E*6*L*Iy / L**3, 0, 0, 0, E*12*Iy / L**3, 0, E*6*L*Iy / L**3, 0],
            [0, 0, 0, -E*G*J*L**2 / (E*L**3), 0, 0, 0, 0, 0, E*G*J*L**2 / (E*L**3), 0, 0],
            [0, 0, -E*6*L*Iy / L**3, 0, E*2*L**2*Iy / L**3, 0, 0, 0, E*6*L*Iy / L**3, 0, E*4*L**2*Iy / L**3, 0],
            [0, E*6*L*Iz / L**3, 0, 0, 0, E*2*L**2*Iz / L**3, 0, -E*6*L*Iz / L**3, 0, 0, 0, E*4*L**2*Iz / L**3]
])

        if self.theta_x ==0 and self.theta_z == 0:
            a11 = 0
            a12 = self.theta_y
            a13 = 0

            a21 = -self.theta_y * np.cos(self.rotate)
            a22 = 0
            a23 = np.sin(self.rotate)

            a31 = self.theta_y * np.sin(self.rotate)
            a32 = 0
            a33 = np.cos(self.rotate)

        else:

            a11 = self.theta_x
            a12 = self.theta_y
            a13 = self.theta_z

            a21 = (- self.theta_x * self.theta_y * np.cos(self.rotate) - self.theta_z * np.sin(self.rotate)) / np.sqrt(self.theta_x ** 2 + self.theta_z ** 2)
            a22 = np.sqrt(self.theta_x ** 2 + self.theta_z ** 2) * np.cos(self.rotate)
            a23 = (- self.theta_x * self.theta_z * np.cos(self.rotate) + self.theta_x * np.sin(self.rotate)) / np.sqrt(self.theta_x ** 2 + self.theta_z ** 2)

            a31 = (self.theta_x * self.theta_y * np.sin(self.rotate) - self.theta_z * np.cos(self.rotate)) / np.sqrt(self.theta_x ** 2 + self.theta_z ** 2)
            a32 = - np.sqrt(self.theta_x ** 2 + self.theta_z ** 2) * np.sin(self.rotate)
            a33 = (self.theta_x * self.theta_y * np.sin(self.rotate) + self.theta_x * np.cos(self.rotate)) / np.sqrt(self.theta_x ** 2 + self.theta_z ** 2)

        self.T = sp.Matrix([[a11, a12, a13, 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  ],
                            [a21, a22, a23, 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  ],
                            [a31, a32, a33, 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  ],
                            [0  , 0  , 0  , a11, a12, a13, 0  , 0  , 0  , 0  , 0  , 0  ],
                            [0  , 0  , 0  , a21, a22, a23, 0  , 0  , 0  , 0  , 0  , 0  ],
                            [0  , 0  , 0  , a31, a32, a33, 0  , 0  , 0  , 0  , 0  , 0  ],
                            [0  , 0  , 0  , 0  , 0  , 0  , a11, a12, a13, 0  , 0  , 0  ],
                            [0  , 0  , 0  , 0  , 0  , 0  , a21, a22, a23, 0  , 0  , 0  ],
                            [0  , 0  , 0  , 0  , 0  , 0  , a31, a32, a33, 0  , 0  , 0  ],
                            [0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , a11, a12, a13],
                            [0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , a21, a22, a23],
                            [0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , a31, a32, a33]

        ])
        self.A, self.E, self.L, self.Iz = A, E, L, Iz
        self.ke = self.T.T * self.ke_ * self.T

        self.get_forces_vector()
        self.atribuir_graus()

    def get_forces_vector(self):
        node1, node2 = self.list_nodes
        self.f = np.array([node1.fx, node1.fy, node1.mz, node2.fx, node2.fy, node2.mz])    

    def definir_geometria(self):
        node1, node2 = self.list_nodes
        x1, y1, z1, x2, y2, z2 = node1.x, node1.y, node1.z, node2.x, node2.y, node2.z

        length = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2)

        theta_x = (node2.x - node1.x) / length
        theta_y = (node2.y - node1.y) / length
        theta_z = (node2.z - node1.z) / length
        # rotate = np.arctan((node2.y - node1.y) / (node2.z - node1.z))

        if ((node2.z - node1.z) == 0) and ((node2.y - node1.y) > 0):
            rotate = np.pi / 2
        elif ((node2.z - node1.z) == 0) and ((node2.y - node1.y) < 0):
            rotate = 3 * np.pi / 2
        elif ((node2.y - node1.y) == 0) and ((node2.z - node1.z) >= 0):
            rotate = 0
        elif ((node2.y - node1.y) == 0) and ((node2.z - node1.z) < 0):
            rotate = np.pi
        else:
            print(node2.z, node1.z)
            rotate = np.arctan((node2.y - node1.y) / (node2.z - node1.z))
        
        return length, theta_x, theta_y, theta_z, rotate

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