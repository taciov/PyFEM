import tkinter as tk
from tkinter import ttk

from src import Apoio as ap
from src import Modelo as md


class MainWindow(tk.Tk):

    tam_node = 2
    modo = None

    def __init__(self, * args, ** kwargs):
        super().__init__(* args, ** kwargs)

        self.modelo = md.Modelo()

        self.title("PyFEM")
        self.geometry("800x600")
        self.resizable(False, False)

        self.upper_menu = UpperMenu(self, width = 800, height = 100, bg = 'white')
        self.upper_menu.grid(row=0, column = 0, columnspan=2)



        self.frame_criar_node = tk.Frame(self.upper_menu, bg = 'white', bd = 1, highlightthickness=1)
        self.frame_criar_node.grid(row = 0, column = 0)

        self.botao_criar_node_clique = tk.Button(self.frame_criar_node, text= "Mouse", command = self.modo_desenhar_node)
        self.botao_criar_node_clique.grid(row = 0, column = 0)

        self.botao_criar_node_coord = tk.Button(self.frame_criar_node, text= "Teclado", command = self.modo_digitar_node)
        self.botao_criar_node_coord.grid(row = 0, column = 1)


        
        self.frame_criar_bar = tk.Frame(self.upper_menu, bg = 'white', bd = 1, highlightthickness=1)
        self.frame_criar_bar.grid(row = 0, column = 1)

        self.botao_criar_bar = tk.Button(self.frame_criar_bar, text= "Criar Barra", command = self.modo_desenhar_bar)
        self.botao_criar_bar.grid(row = 0, column = 0)



        for child in self.upper_menu.winfo_children():
            for child2 in child.winfo_children():
                child2.grid_configure(padx=2, pady=4)

        self.canvas = tk.Canvas(self, scrollregion=(-1000, -1000, 1000, 1000), width = 800, height = 500, bg = 'white')
        self.canvas.grid(row = 1, column = 1)

        # Bind mouse events for drawing and moving the canvas
        self.canvas.bind("<Button-1>", self.mouse_click)  # Left click for actions
        # self.canvas.bind("<B1-Motion>", self.pan_canvas)  # Dragging with left mouse button
        # self.canvas.bind("<MouseWheel>", self.zoom_canvas)  # Zoom with the mouse wheel
        # self.canvas.bind("<Button-4>", self.zoom_canvas)  # For Linux zoom in
        # self.canvas.bind("<Button-5>", self.zoom_canvas)  # For Linux zoom out
    
        # self.upper_menu
    def modo_desenhar_node(self):

        if self.modo == 'desenhar_node':
            self.modo = None
        else:
            self.modo = "desenhar_node"
    
    def modo_digitar_node(self):

        if self.modo == 'digitar_node':
            self.modo = None
        else:
            self.modo = 'digitar_node'
    
    def modo_desenhar_bar(self):

        self.modo = "criar_linha"
    
    def mouse_click(self, event):

        x, y = self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)

        if self.modo == "desenhar_node":
            self.desenhar_node(x, y)

    def desenhar_node(self, x, y):

        self.canvas.create_oval(x - self.tam_node, 
                                y - self.tam_node, 
                                x + self.tam_node, 
                                y + self.tam_node, 
                                fill = 'black', 
                                outline = 'black')
        
        self.modelo.criar_node(x, y)

class UpperMenu(tk.Frame):

    def __init__(self, container, ** kwargs):
        super().__init__(container, ** kwargs)


root = MainWindow()
root.mainloop()