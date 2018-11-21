import numpy as np
import plotly
import plotly.graph_objs as go

# Horizontal 'h'
ORIENTATION = 'h'

WIDTH = 3

BASE_COLOR = 'rgba(0, 0, 0, {})'
NAME = 'TIME %'

BARCHART_FILE_OUTPUT = 'barchart.html'


class BarChart:
    percentages = None
    gradient = None
    function_names = []

    def __init__(self, lines):
        self.lines = lines

    def _generate_gradient(self):
        print('Generating gradient')
        gradient = list(range(100, 0, -int(100 / len(self.percentages))))
        gradient = [x / 100.0 for x in gradient]
        self.gradient = gradient

    def _filter_data(self):
        print('Filtering data for visualization')
        lines = [x for x in self.lines if x != []]
        np_lines = list(map(lambda line: np.array(line), lines))
        np_lines = list(filter(lambda line: float(line[1]) > 0, np_lines))
        time_function_list = np.array(list(map(lambda line: np.take(line, [1, 5]), np_lines)))
        self.percentages = np.round(time_function_list[:, 0].astype(np.float64) /
                                    np.sum(time_function_list[:, 0].astype(np.float64)) * 100, decimals=1)
        self.function_names = time_function_list[:, 1]

    def _generate_trace(self, x, y, step):
        return go.Bar(
            y=[NAME],
            x=[x],
            name=y,
            orientation=ORIENTATION,
            marker=dict(
                color=BASE_COLOR.format(step),
                line=dict(
                    color=BASE_COLOR.format(step),
                    width=WIDTH)
            )
        )

    def generate_graph(self):
        # TODO: Build graph from varying input size, stacking horizontal bar graphs
        self._filter_data()
        self._generate_gradient()
        traces = []
        print('Generating traces')
        for pcnt, fn, grad in zip(self.percentages, self.function_names, self.gradient):
            traces.append(self._generate_trace(pcnt, fn, grad))
        layout = go.Layout(
            barmode='stack'
        )
        # Online plotting
        # fig = go.Figure(data=traces, layout=layout)
        # py.plot(fig, filename='marker-h-bar')

        plotly.offline.plot({
            "data": traces,
            "layout": layout,
        }, filename=BARCHART_FILE_OUTPUT, auto_open=True)

