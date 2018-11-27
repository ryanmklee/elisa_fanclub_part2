import numpy as np

import viz.builder as vb
import viz.viz_constants as vc
from libs import utils


class VizFactory:
    DEFAULT_LINE = [0] * 6
    FACTORY = {
        vc.HORIZONTAL_BAR_CHART: vb.BarChart,
        vc.TABLE: vb.Table,
        vc.LINE_CHART: vb.LineChart,
        vc.AREA_CHART: vb.AreaChart,
        vc.STACKED_BAR_CHART: vb.StackedBarChart,
        vc.BUBBLE_CHART: vb.BubbleChart
    }

    def render_viz(self, chart_type, headers, n_sizes, iteration_data, render_options):
        print(render_options)
        reverse = render_options["reverse"]
        track = render_options["track"]
        significance = render_options["significance"]
        tottime_idx = headers.index(vc.TOTAL_TIME)
        desc_idx = headers.index(vc.DESCRIPTOR)
        fn_points = {}

        if track:
            # withdraw first iteration to get a filtered list of functions to extract
            baseline_data = self.extract_base_lines(iteration_data[0])
            nonzero_data = filter(lambda line: float(line[tottime_idx]) > 0, baseline_data)
            fn_descriptors = np.array(list(nonzero_data))[:, desc_idx]
            fn_names = self.process_function_names(fn_descriptors)

            for data in iteration_data:
                iter_lines = self.extract_iter_lines(data, fn_descriptors, desc_idx)
                self.add_points(iter_lines, fn_names, fn_points, tottime_idx, significance)
        else:
            all_descriptors = []
            all_lines = []
            iter_lines = []
            for idx, data in enumerate(iteration_data):
                baseline_data = self.extract_base_lines(data)
                named_data = {str(line[desc_idx]): line for line in baseline_data}
                nonzero_data = filter(lambda line: float(line[tottime_idx]) > 0, baseline_data)
                fn_descriptors = np.array(list(nonzero_data))[:, desc_idx]

                new_fns = set(fn_descriptors) - set(all_descriptors)
                all_descriptors.extend(new_fns)
                for fn in new_fns:
                    for i in range(idx):
                        backfill_value = self.get_line(all_lines[i], fn)
                        iter_lines[i].append(backfill_value)

                all_lines.append(named_data)
                iter_lines.append([
                    self.get_line(named_data, descriptor)
                    for descriptor in all_descriptors
                ])

            fn_names = self.process_function_names(all_descriptors)
            for group in iter_lines:  # only contains
                self.add_points(np.array(group), fn_names, fn_points, tottime_idx, significance)

        if reverse:
            self._reverse_entries(n_sizes, fn_points.values())

        fn_np_map = {k: np.array(v) for k, v in fn_points.items()}
        builder = self.FACTORY[chart_type](fn_np_map, n_sizes)
        builder.render()

    def add_points(self, iter_lines, fn_names, fn_points, tottime_idx, significance):
        percentages = list(filter(lambda p: p > significance, self._generate_percentages(iter_lines[:, tottime_idx])))
        gradient = self._generate_gradient(percentages)
        for idx, line in enumerate(iter_lines):
            ncalls = line[vc.NCALL_IDX]
            percall = line[vc.PERCALL_IDX]

            n = fn_names[idx]
            curr = fn_points[n] if n in fn_points else []
            fn_points[n] = curr + [[ncalls, np.array(percentages).item(idx), percall, gradient[idx]]]

    def extract_base_lines(self, data):
        lines = [x for x in data if x != []]
        for l in lines:
            l[5] = ' '.join(l[5:])
            while len(l) > 6:
                l.pop()
        return np.array(list(map(np.array, lines)))

    def extract_iter_lines(self, iteration_data, descriptors, d):
        descriptor_pool = {descriptor: idx for idx, descriptor in enumerate(descriptors)}
        # in case function is never called in non-baseline iterations
        iter_lines = [self.DEFAULT_LINE for _ in range(len(descriptors))]
        for line in iteration_data:
            if line and line[d] in descriptor_pool:
                pool_idx = descriptor_pool[line[d]]
                iter_lines[pool_idx] = np.array(line)
        return np.array(iter_lines)

    def get_line(self, o, attr):
        return o[attr] if attr in o else self.DEFAULT_LINE

    def process_function_names(self, function_names):
        return [utils.extract_constructor(name) or utils.extract_method(name) or name for name in function_names]

    def _generate_percentages(self, tottime_list):
        return np.round(tottime_list.astype(np.float64) /
                        np.sum(tottime_list.astype(np.float64)) * 100, decimals=1)

    def _generate_gradient(self, percentages):
        print('Generating gradient')
        interval = max(100 / len(percentages), 10)
        interval_count = 100 / interval
        subinterval = interval_count / (len(percentages) / interval)
        base_val = 100
        gradient = []
        for i in range(len(percentages)):
            gradient.append(base_val - interval*(i % interval_count) - subinterval*int(i / interval_count))
        return [x / 100.0 for x in gradient]

    def _reverse_entries(self, sizes, fn_points):
        sizes.reverse()

        for point_group in fn_points:
            point_group.reverse()
