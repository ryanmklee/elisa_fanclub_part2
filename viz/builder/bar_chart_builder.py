import plotly.graph_objs as go

from viz.builder.abstract_builder import AbstractViz
import viz.viz_constants as vc

WIDTH = 3
BASE_COLOR = 'rgba(0, 0, 0, {})'


class BarChart(AbstractViz):
    def __init__(self, lines, n_sizes):
        super().__init__(lines, n_sizes)
        self.file_output = vc.BARCHART_FILE_OUTPUT

    def _generate_trace(self, x, y, step):
        return go.Bar(
            y=self.n_sizes,
            x=x,
            name=y,
            orientation=vc.HORIZONTAL_ORIENTATION,
            marker=dict(
                color=BASE_COLOR.format(step),
                line=dict(
                    color=BASE_COLOR.format(step),
                    width=WIDTH)
            )
        )

    def generate_traces(self):
        return [self._generate_trace(pcnt, fn, grad) for pcnt, fn, grad in self.lines]

    def generate_layout(self):
        return go.Layout(
            barmode='stack'
        )
