import numpy as np

import viz.builder as vb
import viz.viz_constants as vc
from libs import utils


class VizFactory:
    FACTORY = {
        vc.HORIZONTAL_BAR_CHART: vb.BarChart,
        vc.TABLE: vb.Table,
        vc.LINE_CHART: vb.LineChart,
        vc.AREA_CHART: vb.AreaChart,
        vc.STACKED_BAR_CHART: vb.StackedBarChart,
        vc.BUBBLE_CHART: vb.BubbleChart
    }

    def render_viz(self, chart_type, headers, n_sizes, iteration_data, reverse):

        # withdraw first iteration to form backbone for processed_lines
        # then add each pcnt to the corresponding backbone entry for each extra iteration
        tottime_idx = headers.index(vc.TOTAL_TIME),
        desc_idx = headers.index(vc.DESCRIPTOR)

        baseline_data = iteration_data[0]
        fn_descriptors = self.extract_base_lines(baseline_data, tottime_idx)[:, desc_idx]
        fn_names = self.process_function_names(fn_descriptors)
        fn_times = {desc: [] for desc in fn_names}

        for data in iteration_data:
            iter_lines = self.extract_iter_lines(data, fn_descriptors, desc_idx)
            percentages = self._generate_percentages(iter_lines[:, tottime_idx])
            gradient = self._generate_gradient(percentages)
            for idx, line in enumerate(iter_lines):
                ncalls = line[vc.NCALL_IDX]
                percall = line[vc.PERCALL_IDX]
                fn_times[fn_names[idx]].append(
                    [ncalls, percentages.item(idx), percall, gradient[idx]]
                )

        # if reverse:
        #     self._reverse_entries(n_sizes, fn_times.values())

        np_times = {k: np.array(v) for k, v in fn_times.items()}
        builder = self.FACTORY[chart_type](np_times, n_sizes)
        builder.render()

    def extract_base_lines(self, data, tottime_idx):
        print('Filtering data for visualization')
        lines = [x for x in data if x != []]
        return np.array(list(filter(
            lambda line: float(line[tottime_idx]) > 0,
            map(np.array, lines)
        )))

    def extract_iter_lines(self, iteration_data, descriptors, d):
        descriptor_pool = {descriptor: idx for idx, descriptor in enumerate(descriptors)}
        # in case function is never called in non-baseline iterations
        iter_lines = [np.array([0] * 6) for _ in range(len(descriptors))]
        for line in iteration_data:
            if line and line[d] in descriptor_pool:
                pool_idx = descriptor_pool[line[d]]
                iter_lines[pool_idx] = np.array(line)
        return np.array(iter_lines)

    def process_function_names(self, function_names):
        return [utils.extract_constructor(name) or utils.extract_method(name) for name in function_names]

    def _generate_percentages(self, tottime_list):
        return np.round(tottime_list[:, 0].astype(np.float64) /
                        np.sum(tottime_list[:, 0].astype(np.float64)) * 100, decimals=1)

    def _generate_gradient(self, percentages):
        print('Generating gradient')
        gradient = list(range(100, 0, -int(100 / len(percentages))))[:len(percentages)]
        return [x / 100.0 for x in gradient]

    def _reverse_entries(self, sizes, lines):
        sizes.reverse()

        for pcnt, fn, grad in lines:
            pcnt.reverse()
