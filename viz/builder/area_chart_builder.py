import plotly.graph_objs as go

from viz.builder.line_chart_builder import LineChart
import viz.viz_constants as vc
from libs.colors import DARK_PALETTE
from libs.utils import format_rgb


class AreaChart(LineChart):
    def __init__(self, lines, n_sizes):
        super().__init__(lines, n_sizes)
        self.file_output = vc.AREACHART_FILE_OUTPUT

    def _generate_trace(self, line, color_idx):
        pcnt, fn, grad = line

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
