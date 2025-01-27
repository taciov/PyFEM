import tkinter as tk
from tkinter import messagebox
from src import Modelo as md

class MainWindow(tk.Tk):

    tam_node = 3.5  # Adjust size for visibility
    modo = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.modelo = md.Modelo()

        self.nodes = []  # To store node coordinates
        self.selected_nodes = []  # To track selected nodes for connection
        self.highlighted_items = []  # To store highlighted oval IDs

        self.title("PyFEM")
        self.geometry("800x600")
        self.resizable(False, False)

        self.upper_menu = UpperMenu(self, width=800, height=100, bg='white')
        self.upper_menu.grid(row=0, column=0, columnspan=2)

        self.frame_criar_node = tk.Frame(self.upper_menu, bg='white', bd=1, highlightthickness=1)
        self.frame_criar_node.grid(row=0, column=0)

        self.botao_criar_node_clique = tk.Button(self.frame_criar_node, text="Mouse", command=self.modo_desenhar_node)
        self.botao_criar_node_clique.grid(row=0, column=0)

        self.botao_criar_node_coord = tk.Button(self.frame_criar_node, text="Teclado", command=self.digitar_node)
        self.botao_criar_node_coord.grid(row=0, column=1)

        self.bota_criar_apoio = tk.Button(self.frame_criar_node, text = "Apoio", command = self.modo_criar_apoio)
        self.bota_criar_apoio.grid(row = 0, column = 2)

        self.frame_criar_bar = tk.Frame(self.upper_menu, bg='white', bd=1, highlightthickness=1)
        self.frame_criar_bar.grid(row=0, column=1)

        self.botao_criar_bar = tk.Button(self.frame_criar_bar, text="Criar Barra", command=self.modo_conectar_nodes)
        self.botao_criar_bar.grid(row=0, column=0)

        for child in self.upper_menu.winfo_children():
            for child2 in child.winfo_children():
                child2.grid_configure(padx=2, pady=4)

        self.canvas = tk.Canvas(self, scrollregion=(-1000, -1000, 1000, 1000), width=800, height=500, bg='white')
        self.canvas.grid(row=1, column=1)

        # Bind mouse events for drawing and moving the canvas
        self.canvas.bind("<Button-1>", self.mouse_click)  # Left click for actions
        self.canvas.bind("<Button-2>", self.start_pan)  # Middle mouse button press
        self.canvas.bind("<B2-Motion>", self.pan_canvas)  # Dragging with middle mouse button
        self.canvas.bind("<ButtonRelease-2>", self.stop_pan)  # Release middle mouse button
    
    def start_pan(self, event):
        """Start panning when the middle mouse button is pressed."""
        self.canvas.scan_mark(event.x, event.y)  # Mark the starting point

    def pan_canvas(self, event):
        """Pan the canvas by dragging the middle mouse button."""
        self.canvas.scan_dragto(event.x, event.y, gain=1)  # Drag to new position

    def stop_pan(self, event):
        """Stop panning when the middle mouse button is released."""
        pass  # No specific action needed, but you can reset state if necessary

    def mouse_click(self, event):
        """Draw a node on the canvas at the clicked position."""
        x, y = self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)
        self.desenhar_node(x, y)

    def modo_desenhar_node(self):
        self.modo = "desenhar_node" if self.modo != "desenhar_node" else None

    def modo_criar_apoio(self):
        self.modo = "criar_apoio" if self.modo != "criar_apoio" else None

    def modo_conectar_nodes(self):
        self.modo = "conectar_nodes" if self.modo != "conectar_nodes" else None

    def mouse_click(self, event):
        x, y = self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)

        if self.modo == "desenhar_node":
            self.desenhar_node(x, y)
        elif self.modo == "conectar_nodes":
            self.selecionar_node(x, y)
        elif self.modo == 'criar_apoio':
            self.selecionar_node(x, y)
            node = self.selected_nodes[0]
            self.criar_apoio(node[0], node[1])

    def desenhar_node(self, x, y):
        # Draw node
        self.canvas.create_oval(
            x - self.tam_node,
            y - self.tam_node,
            x + self.tam_node,
            y + self.tam_node,
            fill='black',
            outline='black',
        )
        # Store node coordinates
        self.nodes.append((x, y))

        self.modelo.criar_node(x, y)

    def selecionar_node(self, x, y):
        # Find the nearest node
        for node in self.nodes:
            if abs(node[0] - x) <= self.tam_node and abs(node[1] - y) <= self.tam_node:
                print(node)
                print(x, y)
                self.selected_nodes.append(node)
                self.highlight_node(node)  # Highlight selected node
                break
        
        if self.modo == 'conectar_nodes':
            # If two nodes are selected, connect them
            if len(self.selected_nodes) == 2:
                self.conectar_nodes()
                self.selected_nodes = []  # Reset selection
                self.clear_highlights()  # Remove highlights


    def conectar_nodes(self):
        # Draw line between the two selected nodes
        x1, y1 = self.selected_nodes[0]
        x2, y2 = self.selected_nodes[1]
        self.canvas.create_line(x1, y1, x2, y2, fill='black', width=1)

        E = 1
        A = 1
        I = 1

        ## Adicionar aqui uma tela na qual seja possível inserir os dados da seção de concreto 

        self.modelo.criar_barra(E, A, I, self.modelo.identif_node(x1, y1), self.modelo.identif_node(x2, y2))

    def highlight_node(self, node):
        # Highlight a selected node
        x, y = node
        highlight = self.canvas.create_oval(
            x - self.tam_node - 2,
            y - self.tam_node - 2,
            x + self.tam_node + 2,
            y + self.tam_node + 2,
            outline='red',
            width=2,
        )
        self.highlighted_items.append(highlight)

    def clear_highlights(self):
        # Remove all highlighted items
        for item in self.highlighted_items:
            self.canvas.delete(item)
        self.highlighted_items = []  # Clear the list of highlighted items

    def digitar_node(self):
        tela = tk.Tk()
        tela.geometry("160x80")
        tela.resizable(False, False)

        frame = tk.Frame(tela, bg='white')
        frame.grid(row=0, column=0)

        label_x = tk.Label(tela, text="X: ")
        label_x.grid(row=0, column=0)

        self.input_x = tk.Entry(tela)
        self.input_x.grid(row=0, column=1)

        label_y = tk.Label(tela, text="Y: ")
        label_y.grid(row=1, column=0)

        self.input_y = tk.Entry(tela)
        self.input_y.grid(row=1, column=1)

        button = tk.Button(tela, text="Criar Node", command=self.get_coordinates)
        button.grid(row=2, column=0, columnspan=2)

        tela.bind("<Return>", lambda event: self.get_coordinates())
        tela.bind("<KP_Enter>", lambda event: self.get_coordinates())

        tela.mainloop()

    def get_coordinates(self):
        try:
            x = float(self.input_x.get())
            y = float(self.input_y.get())
            self.desenhar_node(x, y)
        except ValueError:
            messagebox.showerror("Error", "Please enter valid float numbers!")

    def get_apoio(self):
        self.modelo.criar_apoio([self.glx.get(), self.gly.get(), self.glz.get()], x = self.x, y = self.y)
        self.clear_highlights()
        self.tela.destroy()

    def criar_apoio(self, x, y):

        self.x = x
        self.y = y

        # print(x, y)

        self.tela = tk.Tk()
        self.tela.geometry("260x120")
        self.tela.resizable(False, False)

        self.glx = tk.IntVar()
        self.gly = tk.IntVar()
        self.glz = tk.IntVar()

        label_x = tk.Label(self.tela, text="Deslocamento em X: ")
        label_x.grid(row = 0, column=0)

        grau_x_livre = tk.Radiobutton(self.tela, text = "Livre", variable=self.glx, value=0)
        grau_x_livre.grid(row = 0, column = 1)

        grau_x_fixo = tk.Radiobutton(self.tela, text = "Fixo", variable=self.glx, value=1)
        grau_x_fixo.grid(row = 0, column = 2)

        label_y = tk.Label(self.tela, text="Deslocamento em Y: ")
        label_y.grid(row = 1, column=0)

        grau_y_livre = tk.Radiobutton(self.tela, text = "Livre", variable=self.gly, value=0)
        grau_y_livre.grid(row = 1, column = 1)

        grau_y_fixo = tk.Radiobutton(self.tela, text = "Fixo", variable=self.gly, value=1)
        grau_y_fixo.grid(row = 1, column = 2)

        label_z = tk.Label(self.tela, text="Rotação em Z: ")
        label_z.grid(row = 2, column=0)

        grau_z_livre = tk.Radiobutton(self.tela, text = "Livre", variable=self.glz, value=0)
        grau_z_livre.grid(row = 2, column = 1)

        grau_z_fixo = tk.Radiobutton(self.tela, text = "Fixo", variable=self.glz, value=1)
        grau_z_fixo.grid(row = 2, column = 2)

        button_criar_apoio = tk.Button(self.tela, text = "Criar apoio", command = self.get_apoio)
        button_criar_apoio.grid(row = 3, column = 0, columnspan = 2)

        self.tela.mainloop()


class UpperMenu(tk.Frame):
    def __init__(self, container, **kwargs):
        super().__init__(container, **kwargs)


root = MainWindow()
root.mainloop()
