import cProfile
import pstats
import io
import os


class VizProfiler:
    def __init__(self):
        self.profiler = cProfile.Profile()

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
            iteration_stats.append(self.get_stat_lists()[1])

            size //= scale

        return n_sizes, iteration_stats

    def get_stat_lists(self):
        lines = []
        s = io.StringIO()
        stats = pstats.Stats(self.profiler, stream=s).sort_stats('tottime')
        stats.print_stats()

        # Profile does not expose an API to us to return the list of stats
        # in human readable form. We must read it to disk using a string buffer
        # and read it back in.
        with open('test.txt', 'w+') as f:
            f.write(s.getvalue())

        with open('test.txt', 'r') as f:
            for _ in range(4):
                f.readline()

            headers = [column for column in f.readline().split() if column]

            for line in f:
                if line:
                    if line.find("{") != -1:
                        numbers, fn_name = line.split("{")
                        lines.append(numbers.split() + [fn_name.split("}")[0]])
                    else:
                        lines.append(line.split())

        # cleanup file from disk
        os.remove('test.txt')

        return headers, lines

    def refresh_profiler(self):
        self.profiler = cProfile.Profile()
