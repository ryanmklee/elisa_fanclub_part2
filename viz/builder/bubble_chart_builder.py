import plotly.graph_objs as go

import viz.viz_constants as vc
from viz.builder.abstract_builder import AbstractViz


class BubbleChart(AbstractViz):
    def __init__(self, lines, n_sizes):
        super().__init__(lines, n_sizes)
        self.file_output = vc.BUBBLECHART_FILE_OUTPUT

    def _generate_trace(self, ncalls, pcnt, percall, fn_names, input_size):
        text = []
        for i in range(len(fn_names)):
            text.append(str(pcnt[i]) + '% of total runtime<br>' + str(fn_names[i]))
        return go.Scatter(
            x=ncalls,
            y=percall,
            mode='markers',
            name=input_size,
            text=text,
            marker=dict(
                sizemode='area',
                size=pcnt,
                sizeref=150. / (100 ** 2),
                line=dict(
                    width=2
                ),
                sizemin=7
            )
        )

    def generate_traces(self):
        traces = []
        fn_names = list(self.fn_pts_map.keys())
        fn_points = map(lambda nd: nd.tolist(), self.fn_pts_map.values())
        input_points = list(zip(*fn_points))

        for size in range(len(self.n_sizes)):
            ncalls, pcnt, percall, _ = [list(map(float, ls)) for ls in zip(*input_points[size])]
            # cProfile only saves up to 3 decimal points
            # Zero per-call nodes are not rendered because of the chart's log axis
            # Set to 1us if ncalls > 0 to forcibly render the point
            percall = [num if num or not ncalls[i] else 0.000001 for i, num in enumerate(percall)]
            traces.append(self._generate_trace(ncalls, pcnt, percall, fn_names, self.n_sizes[size]))

        return traces

    def generate_layout(self):
        return go.Layout(
            title='Call Count vs Call Time on Varied Input Sizes',
            xaxis=dict(
                title='Number of Calls',
                type='log',
            ),
            yaxis=dict(
                title='Average Time Per Call',
                type='log',
            )
        )
