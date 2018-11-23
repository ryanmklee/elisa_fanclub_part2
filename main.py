from viz.viz_factory import VizFactory
from viz.viz_profiler import VizProfiler
from libs.benchmark_agent import BenchmarkAgent


if __name__ == '__main__':
    # TODO: CLI tools to perform profiling
    # TODO: Filter data for better formatting
    profiler = VizProfiler()
    n_sizes, iterative_stats, headers = profiler.run_iterations(BenchmarkAgent(), 1000, 10)

    factory = VizFactory()
    print('---Begin visualization of profiled code---')
    factory.render_viz("horizontal_bar", headers, n_sizes, iterative_stats)
