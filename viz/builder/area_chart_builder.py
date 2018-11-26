import plotly.graph_objs as go

import viz.viz_constants as vc
from libs.colors import DARK_PALETTE
from libs.utils import format_rgb
from viz.builder.line_chart_builder import LineChart


class AreaChart(LineChart):
    def __init__(self, lines, n_sizes):
        super().__init__(lines, n_sizes)
        self.file_output = vc.AREACHART_FILE_OUTPUT

    def _generate_trace(self, pcnt, fn, grad, color_idx):
        return go.Scatter(
            x=self.n_sizes,
            y=pcnt,
            name=fn,
            hoverinfo='x+y',
            mode='none',
            fill='tonexty',
            line=dict(
                color=(format_rgb(DARK_PALETTE[color_idx])),
                width=0.5)
        )
