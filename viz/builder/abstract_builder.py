import plotly

from abc import ABC as abstract_class
from abc import abstractmethod


class AbstractViz(abstract_class):
    def __init__(self, lines, n_sizes):
        self.lines = lines
        self.n_sizes = n_sizes
        self.file_output = None

    @abstractmethod
    def generate_traces(self):
        pass

    @abstractmethod
    def generate_layout(self):
        pass

    def plot(self, traces, layout):
        plotly.offline.plot({
            "data": traces,
            "layout": layout,
        }, filename=self.file_output, auto_open=True)

    def render(self):
        traces = self.generate_traces()
        layout = self.generate_layout()

        # fig = go.Figure(data=traces, layout=layout)
        # py.plot(fig, filename='marker-h-bar')

        self.plot(traces, layout)

