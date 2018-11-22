import os

import plotly.plotly as py
import plotly.io as pio
import plotly.graph_objs as go

from viz.builder.horizontal_bar_chart_builder import BarChart
from viz.viz_profiler import VizProfiler
from libs.benchmark_agent import BenchmarkAgent


def visualize_runtime(lines):
    lines = [x for x in lines if x != []]
    np_lines = list(map(lambda line: np.array(line), lines))
    np_lines = list(filter(lambda line: float(line[1]) > 0, np_lines))
    # TODO: make magic numbers go away
    time_function_list = np.array(list(map(lambda line: np.take(line, [1, 5]), np_lines)))

    top_labels = time_function_list[:, 1]
    x_data = [time_function_list[:, 0].astype(np.float64)]
    y_data = ['Time']

    generate_graph(top_labels, x_data, y_data)


def generate_graph(top_labels, x_data, y_data):
    # Layout code
    colors = ['rgba(38, 24, 74, 0.8)', 'rgba(71, 58, 131, 0.8)',
              'rgba(122, 120, 168, 0.8)', 'rgba(164, 163, 204, 0.85)',
              'rgba(190, 192, 213, 1)']
    traces = []
    for i in range(0, len(x_data[0])):
        for xd, yd in zip(x_data, y_data):
            traces.append(go.Bar(
                x=[xd[i]],
                y=[yd],
                orientation='h',
                marker=dict(
                    # TODO: create colour intensity, not just taking the first color based on x values
                    color=colors[0],
                    line=dict(
                        color='rgb(248, 248, 249)',
                        width=1)
                )
            ))
    layout = go.Layout(
        xaxis=dict(
            showgrid=False,
            showline=False,
            showticklabels=False,
            zeroline=False,
            domain=[0.15, 1]
        ),
        yaxis=dict(
            showgrid=False,
            showline=False,
            showticklabels=False,
            zeroline=False,
        ),
        barmode='stack',
        paper_bgcolor='rgb(248, 248, 255)',
        plot_bgcolor='rgb(248, 248, 255)',
        margin=dict(
            l=120,
            r=10,
            t=140,
            b=80
        ),
        showlegend=False,
    )
    annotations = []
    for yd, xd in zip(y_data, x_data):
        # labeling the y-axis
        annotations.append(dict(xref='paper', yref='y',
                                x=0.14, y=yd,
                                xanchor='right',
                                text=str(yd),
                                font=dict(family='Arial', size=14,
                                          color='rgb(67, 67, 67)'),
                                showarrow=False, align='right'))
        # labeling the first percentage of each bar (x_axis)
        annotations.append(dict(xref='x', yref='y',
                                x=xd[0] / 2, y=yd,
                                text=str(xd[0]) + 's',
                                font=dict(family='Arial', size=14,
                                          color='rgb(248, 248, 255)'),
                                showarrow=False))
        # labeling the first Likert scale (on the top)
        if yd == y_data[-1]:
            annotations.append(dict(xref='x', yref='paper',
                                    x=xd[0] / 2, y=1.1,
                                    text=top_labels[0],
                                    font=dict(family='Arial', size=14,
                                              color='rgb(67, 67, 67)'),
                                    showarrow=False))
        space = xd[0]
        for i in range(1, len(xd)):
            # labeling the rest of percentages for each bar (x_axis)
            annotations.append(dict(xref='x', yref='y',
                                    x=space + (xd[i] / 2), y=yd,
                                    text=str(xd[i]) + 's',
                                    font=dict(family='Arial', size=14,
                                              color='rgb(248, 248, 255)'),
                                    showarrow=False))
            # labeling the Likert scale
            if yd == y_data[-1]:
                annotations.append(dict(xref='x', yref='paper',
                                        x=space + (xd[i] / 2), y=1.1,
                                        text=top_labels[i],
                                        font=dict(family='Arial', size=14,
                                                  color='rgb(67, 67, 67)'),
                                        showarrow=False))
            space += xd[i]
    layout['annotations'] = annotations
    fig = go.Figure(data=traces, layout=layout)
    py.plot(fig, filename='bar-colorscale')
    if not os.path.exists('images'):
        os.mkdir('images')
    pio.write_image(fig, 'images/fig1.png')


if __name__ == '__main__':
    # TODO: CLI tools to perform profiling
    # TODO: Filter data for better formatting
    profiler = VizProfiler()
    profiler.run(BenchmarkAgent())
    headers, lines = profiler.get_stat_lists()

    # visualize_runtime(lines) TODO: Remove this if we dont need it later
    print('---Begin visualization of profiled code---')
    bar = BarChart(lines)
    bar.generate_graph()
