"""
General drawing methods for graphs using Bokeh.
"""
from graph import Graph
from sys import argv
from random import choice, random, sample
from bokeh.io import show, output_file
from bokeh.plotting import figure
from bokeh.models import (GraphRenderer, StaticLayoutProvider, Circle, LabelSet,
                          ColumnDataSource, VeeHead, Arrow)


class BokehGraph:
    """Class that takes a graph and exposes drawing methods."""
    def __init__(self, graph, title='Graph', width=10, height=10,
                show_axis=False, show_grid=False, circle_size=45, 
                draw_components=False):
        if not graph.vertices:
            raise Exception('Graph should contain vertices!')
        self.graph = graph

        # Setup plot
        self.width = width
        self.height = height
        self.pos = {}  # dict to map vertices to x, y positions
        self.plot = figure(title=title, x_range=(0, width), y_range=(0, height))
        self.plot.axis.visible = show_axis
        self.plot.grid.visible = show_grid
        self._setup_graph_renderer(circle_size, draw_components)

    def show(self, output_path='./graph.html'):
        output_file(output_path)
        show(self.plot)

    def _setup_graph_renderer(self, circle_size,draw_components):
        graph_renderer = GraphRenderer()

        graph_renderer.node_renderer.data_source.add(list(self.graph.vertices.keys()), 'index')
        # graph_renderer.node_renderer.data_source.add(self._get_random_colors(), 'color')        
        graph_renderer.node_renderer.glyph = Circle(size=circle_size, fill_color='color')
        # graph_renderer.edge_renderer.data_source.data = self._get_edge_indexes()
        # self.randomize()

        for i in range(len(graph_renderer.edge_renderer.data_source.data["start"])):
            self.plot.add_layout(
                Arrow(
                    end=VeeHead(fill_color="black", size=10),
                    x_start=self.pos[
                        graph_renderer.edge_renderer.data_source.data["start"][i]
                    ][0],
                    y_start=self.pos[
                        graph_renderer.edge_renderer.data_source.data["start"][i]
                    ][1],
                    x_end=self.pos[
                        graph_renderer.edge_renderer.data_source.data["end"][i]
                    ][0],
                    y_end=self.pos[
                        graph_renderer.edge_renderer.data_source.data["end"][i]
                    ][1],
                )
            )


        graph_renderer.layout_provider = StaticLayoutProvider(graph_layout=self.pos)
        self.plot.renderers.append(graph_renderer)
        # self._setup_labels()
    
    def _get_random_colors(self, num_colors=None):
        colors = []
        for _ in range(len(self.graph.vertices)):
            color = '#'+''.join([choice('0123456789ABCDEF') for j in range(6)])
            colors.append(color)
        return colors

    

graph = Graph()  
graph.add_vertex('0')
graph.add_vertex('1')
graph.add_vertex('2')
graph.add_vertex('3')
graph.add_vertex('4')
graph.add_vertex('5')
graph.add_edge('0', '1', False)
graph.add_edge('0', '3', False)
graph.add_edge('1', '2', False)
graph.add_edge('0', '2', False)
graph.add_edge('0', '2')
graph.add_edge('4', '5')
# print(graph.search('1', '3'))

# print(graph.search)

bg = BokehGraph(graph, draw_components=False)
bg.show()