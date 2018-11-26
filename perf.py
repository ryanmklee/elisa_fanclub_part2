import argparse

import viz.viz_utils as vu
from libs.benchmark_agent import BenchmarkAgent
from viz.viz_factory import VizFactory
from viz.viz_profiler import VizProfiler

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--chart', required=True, nargs=3,
                        help='Takes chart type, max input size, and reduction scale')
    parser.add_argument('-r', '--reverse', help="reverse ordering of profile entries",
                        action="store_true")
    args = parser.parse_args()

    chart_options = args.chart
    reverse = args.reverse

    if not vu.check_chart_args(chart_options):
        raise argparse.ArgumentTypeError("Illegal arguments detected, see --help")

    profiler = VizProfiler()
    n_sizes, iterative_stats, headers = profiler.run_iterations(BenchmarkAgent(),
                                                                int(chart_options[1]), int(chart_options[2]))

    factory = VizFactory()
    print('---Begin visualization of profiled code---')

    factory.render_viz(chart_options[0], headers, n_sizes, iterative_stats, reverse)
