import plotly.graph_objs as go

import viz.viz_constants as vc
from viz.builder.abstract_builder import AbstractViz


class Table(AbstractViz):
    def __init__(self, lines, n_sizes):
        super().__init__(lines, n_sizes)
        self.file_output = vc.TABLE_FILE_OUTPUT

    def generate_traces(self):
        header_values = [['<b>INPUT SIZES</b>']]
        header_values.extend([[fn] for fn in self.fn_pts_map.keys()])
        cell_values = [self.n_sizes] + [times[:, 1] for times in self.fn_pts_map.values()]

        trace = go.Table(
            header=dict(
                values=header_values,
                line=dict(color='#506784'),
                fill=dict(color='#05668D'),
                align=['left', 'center'],
                font=dict(color='white', size=12),
                height=40
            ),
            cells=dict(
                values=cell_values,
                line=dict(color='#506784'),
                fill=dict(color=['#F0F3BD', 'white']),
                align=['left', 'center'],
                font=dict(color='#506784', size=12),
                height=30
            ))

        return [trace]

    def generate_layout(self):
        return dict(title="Performance Summary")
