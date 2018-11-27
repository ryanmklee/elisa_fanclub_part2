import plotly.graph_objs as go

import viz.viz_constants as vc
from libs.colors import DARK_PALETTE
from libs.utils import format_rgb
from viz.builder.abstract_builder import AbstractViz


class LineChart(AbstractViz):
    def __init__(self, lines, n_sizes):
        super().__init__(lines, n_sizes)
        self.file_output = vc.LINECHART_FILE_OUTPUT

    def _generate_trace(self, pcnt, fn, grad, color_idx):
        return go.Scatter(
            x=self.n_sizes,
            y=pcnt,
            name=fn,
            line=dict(
                color=(format_rgb(DARK_PALETTE[color_idx])),
                width=4)
        )

    def generate_traces(self):
        traces = []
        for color_idx, fn in enumerate(self.fn_pts_map):
            pcnt = self.fn_pts_map[fn][:, 1]
            grad = self.fn_pts_map[fn][0, 3]
            traces.append(self._generate_trace(pcnt, fn, grad, color_idx))
        return traces

    def generate_layout(self):
        return dict(title='Changes in % Time with Input',
                    xaxis=dict(title='% of Total Time Taken'),
                    yaxis=dict(title='Input Size'),
                    )
