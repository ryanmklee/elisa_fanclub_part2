import plotly.graph_objs as go

from viz.builder.bar_chart_builder import BarChart
import viz.viz_constants as vc


class StackedBarChart(BarChart):
    def __init__(self, lines, n_sizes):
        super().__init__(lines, n_sizes)
        self.file_output = vc.STACKEDBARCHART_FILE_OUTPUT

    def _generate_trace(self, pcnt, fn, step):
        return go.Bar(
            x=self.n_sizes,
            y=pcnt,
            name=fn
        )

