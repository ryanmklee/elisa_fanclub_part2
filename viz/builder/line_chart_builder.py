import plotly.graph_objs as go

from viz.builder.abstract_builder import AbstractViz
import viz.viz_constants as vc
from libs.colors import DARK_PALETTE
from libs.utils import format_rgb


class LineChart(AbstractViz):
    def __init__(self, lines, n_sizes):
        super().__init__(lines, n_sizes)
        self.file_output = vc.LINECHART_FILE_OUTPUT

    def _generate_trace(self, line, color_idx):
        pcnt, fn, grad = line

        return go.Scatter(
            x=self.n_sizes,
            y=pcnt,
            name=fn,
            line=dict(
                color=(format_rgb(DARK_PALETTE[color_idx])),
                width=4)
        )

    def generate_traces(self):
        return [self._generate_trace(line, idx) for idx, line in enumerate(self.lines)]

    def generate_layout(self):
        return dict(title='Changes in % Time with Input',
                    xaxis=dict(title='Input Size'),
                    yaxis=dict(title='% of Total Time Taken'),
                    )
