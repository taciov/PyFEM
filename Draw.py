import tkinter as tk
import json

class DrawApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Draw Points and Connect Lines")
        
        # Create a frame for the side menu
        self.menu_frame = tk.Frame(root, width=200, bg="lightgray")
        self.menu_frame.pack(side=tk.TOP, fill=tk.X)

        # Add control buttons to the side menu
        self.create_point_button = tk.Button(self.menu_frame, text="Create Point", command=self.set_create_point_mode, width=20)
        self.create_point_button.pack(side = tk.LEFT, padx=10, pady = 10)

        self.add_by_coords_button = tk.Button(self.menu_frame, text="Add Point by Coordinates", command=self.show_add_point_by_coords, width=20)
        self.add_by_coords_button.pack(side = tk.LEFT, padx=10, pady = 10)

        self.connect_points_button = tk.Button(self.menu_frame, text="Create line", command=self.set_connect_points_mode, width=20)
        self.connect_points_button.pack(side = tk.LEFT, padx=10, pady = 10)

        self.export_button = tk.Button(self.menu_frame, text="Export to JSON", command=self.export_to_json, width=20)
        self.export_button.pack(side = tk.LEFT, padx=10, pady = 10)

        # Add input fields for coordinates (hidden by default)
        self.coord_frame = tk.Frame(self.menu_frame, bg="lightgray")
        self.x_label = tk.Label(self.coord_frame, text="X:", bg="lightgray")
        self.x_entry = tk.Entry(self.coord_frame, width=10)
        self.y_label = tk.Label(self.coord_frame, text="Y:", bg="lightgray")
        self.y_entry = tk.Entry(self.coord_frame, width=10)
        self.add_point_button = tk.Button(self.coord_frame, text="Add Point", command=self.add_point_by_coords)
        self.coord_frame.pack_forget()

        # Create the drawing canvas
        self.canvas = tk.Canvas(root, width=800, height=600, bg="white", scrollregion=(0, 0, 2000, 2000))
        self.canvas.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)

        # Add scrollbars
        self.h_scroll = tk.Scrollbar(root, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.h_scroll.pack(side=tk.BOTTOM, fill=tk.X)
        self.v_scroll = tk.Scrollbar(root, orient=tk.VERTICAL, command=self.canvas.yview)
        self.v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.configure(xscrollcommand=self.h_scroll.set, yscrollcommand=self.v_scroll.set)

        # Initialize variables
        self.points = []  # List of points as (x, y)
        self.point_ids = {}  # Map of canvas item ID to point index
        self.lines = []  # List of lines as ((x1, y1), (x2, y2))
        self.selected_points = []  # List to store selected points for line drawing
        self.highlight_ids = []  # List to store IDs of highlight ovals
        self.mode = "create_point"  # Current mode: create_point or connect_points

        # Bind mouse events for drawing and moving the canvas
        self.canvas.bind("<Button-1>", self.handle_click)  # Left click for actions
        self.canvas.bind("<B1-Motion>", self.pan_canvas)  # Dragging with left mouse button
        self.canvas.bind("<MouseWheel>", self.zoom_canvas)  # Zoom with the mouse wheel
        self.canvas.bind("<Button-4>", self.zoom_canvas)  # For Linux zoom in
        self.canvas.bind("<Button-5>", self.zoom_canvas)  # For Linux zoom out

        # Variables for panning
        self.pan_start_x = 0
        self.pan_start_y = 0

    def handle_click(self, event):
        """Handle click events on the canvas."""
        x, y = self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)
        if self.mode == "create_point":
            self.add_point(x, y)
        elif self.mode == "connect_points":
            self.connect_point(x, y)

    def set_create_point_mode(self):
        """Switch to 'Create Point' mode."""
        self.mode = "create_point"
        print("Mode: Create Point")

    def set_connect_points_mode(self):
        """Switch to 'Connect Points' mode."""
        self.mode = "connect_points"
        print("Mode: Connect Points")

    def show_add_point_by_coords(self):
        """Show input fields to add a point by coordinates."""
        # self.coord_frame.pack(pady=10)
        # self.x_label.grid(row=0, column=0, padx=5, pady=5)
        # self.x_entry.grid(row=0, column=1, padx=5, pady=5)
        # self.y_label.grid(row=1, column=0, padx=5, pady=5)
        # self.y_entry.grid(row=1, column=1, padx=5, pady=5)
        # self.add_point_button.grid(row=0, column=2, columnspan=2, pady=10)

        coord_window = tk.Toplevel(self.root)
        coord_window.title("Add Point by Coordinates")
        coord_window.geometry("300x150")

        # Create labels and entry fields for X and Y coordinates
        tk.Label(coord_window, text="Enter X Coordinate:").pack(pady=5)
        x_entry = tk.Entry(coord_window, width=10)
        x_entry.pack(pady=5)

        tk.Label(coord_window, text="Enter Y Coordinate:").pack(pady=5)
        y_entry = tk.Entry(coord_window, width=10)
        y_entry.pack(pady=5)

    def add_point_by_coords(self):
        """Add a point using the entered coordinates."""
        try:
            x = float(self.x_entry.get())
            y = float(self.y_entry.get())
            self.add_point(x, y)
            self.x_entry.delete(0, tk.END)
            self.y_entry.delete(0, tk.END)
        except ValueError:
            print("Invalid input: Please enter valid integers for X and Y coordinates.")

    def connect_point(self, x, y):
        """Handle connecting points."""
        clicked_point = self.get_clicked_point(x, y)
        if clicked_point is not None:
            self.selected_points.append(clicked_point)
            self.highlight_point(clicked_point)

            if len(self.selected_points) == 2:
                p1, p2 = self.selected_points
                self.draw_line(p1, p2)
                self.clear_highlights()
                self.selected_points = []

    def get_clicked_point(self, x, y):
        """Check if a point was clicked within a small radius."""
        for index, (px, py) in enumerate(self.points):
            if abs(px - x) <= 5 and abs(py - y) <= 5:
                return index
        return None

    def add_point(self, x, y):
        """Add a point to the canvas."""
        point_id = self.canvas.create_oval(x-5, y-5, x+5, y+5, fill="black")
        self.points.append((x, y))
        self.point_ids[point_id] = len(self.points) - 1

    def highlight_point(self, point_index):
        """Highlight a selected point."""
        x, y = self.points[point_index]
        highlight_id = self.canvas.create_oval(x-7, y-7, x+7, y+7, outline="red", width=2)
        self.highlight_ids.append(highlight_id)

    def clear_highlights(self):
        """Remove all highlight ovals."""
        for highlight_id in self.highlight_ids:
            self.canvas.delete(highlight_id)
        self.highlight_ids = []

    def draw_line(self, point1_index, point2_index):
        """Draw a line between two points."""
        x1, y1 = self.points[point1_index]
        x2, y2 = self.points[point2_index]
        self.canvas.create_line(x1, y1, x2, y2, fill="blue", width=2)
        self.lines.append(((x1, y1), (x2, y2)))

    def export_to_json(self):
        """Export points and lines to a JSON file."""
        data = {
            "points": self.points,
            "lines": self.lines
        }
        with open("drawing.json", "w") as file:
            json.dump(data, file, indent=4)
        print("Exported to drawing.json")

    def pan_canvas(self, event):
        """Pan the canvas using the left mouse button."""
        self.canvas.scan_dragto(event.x, event.y, gain=1)

    def zoom_canvas(self, event):
        """Zoom in or out on the canvas."""
        scale_factor = 1.1 if event.delta > 0 else 0.9  # Zoom in or out
        self.canvas.scale("all", self.canvas.canvasx(event.x), self.canvas.canvasy(event.y), scale_factor, scale_factor)
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

# Create the GUI application
if __name__ == "__main__":
    root = tk.Tk()
    app = DrawApp(root)
    root.mainloop()