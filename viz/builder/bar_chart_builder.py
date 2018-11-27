import plotly.graph_objs as go

import viz.viz_constants as vc
from viz.builder.abstract_builder import AbstractViz


class BarChart(AbstractViz):
    WIDTH = 3
    BASE_COLOR = 'hsv({}, 60%, 100%)'

    def __init__(self, lines, n_sizes):
        super().__init__(lines, n_sizes)
        self.file_output = vc.BARCHART_FILE_OUTPUT

    def _generate_trace(self, x, y, step):
        step *= 255
        return go.Bar(
            y=self.n_sizes,
            x=x,
            name=y,
            orientation=vc.HORIZONTAL_ORIENTATION,
            marker=dict(
                color=self.BASE_COLOR.format(step),
                line=dict(
                    color=self.BASE_COLOR.format(step),
                    width=self.WIDTH)
            )
        )

    def generate_traces(self):
        traces = []
        for fn, times in self.fn_pts_map.items():
            pcnt = times[:, 1]
            grad = times[0, 3]
            traces.append(self._generate_trace(pcnt, fn, grad))
        return traces

    def generate_layout(self):
        return go.Layout(
            barmode='stack',
            xaxis=dict(title='Input Size'),
            yaxis=dict(title='% of Total Time Taken'),
        )

