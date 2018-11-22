import plotly
import plotly.graph_objs as go

# Horizontal 'h'
ORIENTATION = 'h'

WIDTH = 3

BASE_COLOR = 'rgba(0, 0, 0, {})'
NAME = 'TIME %'

BARCHART_FILE_OUTPUT = 'barchart.html'


class BarChart:
    def __init__(self, lines, n_sizes):
        # TODO: We should only be setting percentages, and function names in the constructor remove when we filter
        # TODO: outside of the class
        self.lines = lines
        self.n_sizes = n_sizes

    def _generate_trace(self, x, y, step):
        return go.Bar(
            y=self.n_sizes,
            x=x,
            name=y,
            orientation=ORIENTATION,
            marker=dict(
                color=BASE_COLOR.format(step),
                line=dict(
                    color=BASE_COLOR.format(step),
                    width=WIDTH)
            )
        )

    def render(self):
        # TODO: Build graph from varying input size, stacking horizontal bar graphs
        traces = [self._generate_trace(pcnt, fn, grad) for pcnt, fn, grad in self.lines]

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

