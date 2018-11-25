import cProfile
import pstats
import io


class VizProfiler:
    def __init__(self):
        self.profiler = cProfile.Profile()
        self.headers = None

    def run(self, agent, size):
        agent.run_before(size)

        print('---Beginning profiler---\n')
        self.profiler.enable()
        agent.run_profile()
        self.profiler.disable()
        print('---Finished profiling---')

        agent.run_after()

    def run_iterations(self, agent, size, scale):
        iteration_stats = []
        n_sizes = []

        while size >= scale:
            n_sizes.append("N = " + str(size))
            self.refresh_profiler()
            self.run(agent, size)
            iteration_stats.append(self.get_stat_lists())

            size //= scale

        return n_sizes, iteration_stats, self.headers

    def get_stat_lists(self):
        lines = []
        s = io.StringIO()
        stats = pstats.Stats(self.profiler, stream=s).sort_stats('tottime')
        stats.print_stats()

        raw_lines = [l for l in s.getvalue().splitlines()[4:]]
        headers = [column for column in raw_lines.pop(0).split() if raw_lines]

        for line in raw_lines:
            if line:
                if line.find("{") != -1:
                    numbers, fn_name = line.split("{")
                    lines.append(numbers.split() + [fn_name[:-1]])
                else:
                    lines.append(line.split())

        if self.headers is None:
            self.headers = headers

        return lines

    def refresh_profiler(self):
        self.profiler = cProfile.Profile()
