from viz.viz_factory import VizFactory
from viz.viz_profiler import VizProfiler
from libs.benchmark_agent import BenchmarkAgent


if __name__ == '__main__':
    # TODO: CLI tools to perform profiling
    # TODO: Filter data for better formatting
    profiler = VizProfiler()
    profiler.run(BenchmarkAgent())
    headers, lines = profiler.get_stat_lists()

    factory = VizFactory()
    print('---Begin visualization of profiled code---')
    factory.render_viz("horizontal_bar", lines)
