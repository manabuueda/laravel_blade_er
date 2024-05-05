import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx
from networkx.drawing.nx_agraph import read_dot


class BladeGraphApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Blade File Dependency Graph')
        self.geometry('1000x800')

        self.load_button = tk.Button(self, text="Load .dot File", command=self.load_dot_file)
        self.load_button.pack(pady=20)

        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, self)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill=tk.BOTH, expand=True)

    def load_dot_file(self):
        filepath = filedialog.askopenfilename(title="Select .dot file", filetypes=[("DOT files", "*.dot")])
        if filepath:
            self.display_graph(filepath)

    def display_graph(self, dot_path):
        self.G = read_dot(dot_path)
        self.ax.clear()
        pos = nx.nx_agraph.graphviz_layout(self.G, prog='dot')
        nx.draw(self.G, pos, ax=self.ax, with_labels=True, node_color='lightblue', arrows=True)
        self.canvas.draw()
        self.canvas.mpl_connect('pick_event', self.on_pick)

    def on_pick(self, event):
        artist = event.artist
        if isinstance(artist, nx.Node):
            node = artist.get_label()
            color = 'red' if self.G.nodes[node].get('color', 'lightblue') == 'lightblue' else 'lightblue'
            nx.set_node_attributes(self.G, {node: color}, 'color')
            self.display_graph(dot_path)  # Re-render the graph with updated colors


if __name__ == "__main__":
    app = BladeGraphApp()
    app.mainloop()
