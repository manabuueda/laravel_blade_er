import math
import sys

import pygraphviz as pgv
from PyQt5.QtCore import QPointF, QLineF
from PyQt5.QtGui import QPainter, QPen, QBrush, QColor, QPolygonF
from PyQt5.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QPushButton


def create_graph(file_path):
    G = pgv.AGraph(file_path)
    G.layout(prog='dot')
    return G


class GraphVisualizer(QGraphicsView):
    def __init__(self, graph):
        super().__init__()
        self.graph = graph
        self.scene = QGraphicsScene(self)
        self.scene.setBackgroundBrush(QBrush(QColor(255, 255, 255)))
        self.setScene(self.scene)
        self.setRenderHint(QPainter.Antialiasing)
        self.node_buttons = {}
        self.edges = []
        self.populate_graph()

    def populate_graph(self):
        for node in self.graph.nodes():
            attrs = self.graph.get_node(node).attr
            label = attrs['label'].strip('"')
            pos = attrs.get('pos', '0,0').split(',')
            x, y = map(float, pos)
            button = QPushButton(label)
            button.setStyleSheet("background-color: lightblue; color: black; border: 1px solid black;")
            proxy = self.scene.addWidget(button)
            proxy.setPos(x - button.width() / 2, y - button.height() / 2)
            button.clicked.connect(lambda checked, node=node: self.highlight_connected(node))
            self.node_buttons[node] = (button, proxy)

        # Draw edges before nodes
        for edge in self.graph.edges():
            start, end = edge
            start_point = self.get_position(start)
            end_point = self.get_position(end)
            line = QLineF(start_point, end_point)
            line_item = self.scene.addLine(line, QPen(QColor('black'), 2))
            line_item.setZValue(-10)  # Ensure lines are behind nodes
            self.add_arrow_head(line_item, start_point, end_point)
            self.edges.append((line_item, start, end))

    def get_position(self, node_id):
        pos = self.graph.get_node(node_id).attr.get('pos', '0,0').split(',')
        return QPointF(float(pos[0]), float(pos[1]))

    def add_arrow_head(self, line_item, start_point, end_point):
        angle = math.atan2(end_point.y() - start_point.y(), end_point.x() - start_point.x())
        arrow_size = 10
        arrow_angle = math.pi / 6
        p1 = end_point - QPointF(math.cos(angle - arrow_angle) * arrow_size, math.sin(angle - arrow_angle) * arrow_size)
        p2 = end_point - QPointF(math.cos(angle + arrow_angle) * arrow_size, math.sin(angle + arrow_angle) * arrow_size)
        arrow = QPolygonF([end_point, p1, p2])
        arrow_item = self.scene.addPolygon(arrow, QPen(QColor('black')), QBrush(QColor('black')))
        arrow_item.setZValue(-10)  # Ensure arrow heads are also behind nodes

    def highlight_connected(self, node):
        # Reset all styles
        for button, proxy in self.node_buttons.values():
            button.setStyleSheet("background-color: lightblue; color: black; border: 1px solid black;")
        for line_item, start, end in self.edges:
            line_item.setPen(QPen(QColor('black'), 2))

        # Highlight the selected node and its direct connections
        self.node_buttons[node][0].setStyleSheet("background-color: red; color: white; border: 1px solid black;")
        for edge, start, end in self.edges:
            if start == node or end == node:
                edge.setPen(QPen(QColor('red'), 3))
                self.node_buttons[start][0].setStyleSheet(
                    "background-color: green; color: white; border: 1px solid black;")
                self.node_buttons[end][0].setStyleSheet(
                    "background-color: green; color: white; border: 1px solid black;")


def main():
    app = QApplication(sys.argv)
    graph = create_graph('dependency_graph.dot')
    viewer = GraphVisualizer(graph)
    viewer.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
