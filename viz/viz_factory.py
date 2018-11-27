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
        vc.STACKED_BAR_CHART: vb.StackedBarChart
    }

    def render_viz(self, chart_type, headers, n_sizes, iteration_data, render_options):
        print(render_options)
        reverse = render_options["reverse"]
        track = render_options["track"]
        significance = render_options["significance"]

        if not track:
            chart_data = []
            all_fns = []
            for i in range(len(iteration_data)):
                data = iteration_data[i]
                percentages, fn_names, fn_descriptors = self.extract_base_functions(data, significance)
                zipped_data = {n: p for n, p in zip(fn_names, percentages)}

                new_fns = set(fn_names) - set(all_fns)
                all_fns += list(new_fns)
                for cd in chart_data:
                    fn = cd[1]
                    if fn in fn_names:
                        cd[0].append(zipped_data[fn])
                    else:
                        cd[0].append(0)
                for n, p in zipped_data.items():
                    if n in new_fns:
                        filler = [0 for _ in range(i)]
                        filler.append(p)
                        chart_data.append([filler, n])
            gradient = self._generate_gradient(all_fns)
            for cd in chart_data:
                cd.append(gradient.pop(0))
        else:
            # withdraw first iteration to form backbone for processed_lines
            # then add each pcnt to the corresponding backbone entry for each extra iteration
            baseline_data = iteration_data[0]
            percentages, fn_names, fn_descriptors = self.extract_base_functions(baseline_data, significance)
            gradient = self._generate_gradient(percentages)
            chart_data = [([pcnt], fn, grad) for pcnt, fn, grad in
                               zip(percentages, fn_names, gradient)]

            for idx in range(1, len(iteration_data)):
                line_percentages = self.extract_iteration_percentages(iteration_data[idx], headers, fn_descriptors)
                for i, pcnt in enumerate(line_percentages):
                    chart_data[i][0].append(pcnt)

            if reverse:
                self._reverse_entries(n_sizes, chart_data)

        builder = self.FACTORY[chart_type](chart_data, n_sizes)
        builder.render()

    # returns 3-tuple with relevant functions we want to analyze
    # list of percentages, list of processed function names, list of their raw names for later iterations
    def extract_base_functions(self, data, significance):
        print('Filtering data for visualization')
        lines = [x for x in data if x != []]
        for l in lines:
            l[5] = ' '.join(l[5:])
        np_lines = list(map(lambda line: np.array(line), lines))
        np_lines = list(filter(lambda line: float(line[1]) > 0, np_lines))
        time_function_list = np.array(list(map(lambda line: np.take(line, [1, 5]), np_lines)))
        percentages = list(filter(lambda p: p > significance, self._generate_percentages(time_function_list)))
        function_names = self.process_function_names(time_function_list[:, 1])

        return percentages, function_names, time_function_list[:, 1]

    # separate function to generate percentages for subsequent iterations beyond the first
    # because our extractor function excludes lines with runtime = 0
    # this is incorrect behavior for other iterations as we are still interested in them
    # the line itself may be absent, which is why times_function_list has placeholder np.arrays
    def extract_iteration_percentages(self, data, headers, descriptors):
        descriptor_pool = {descriptor: idx for idx, descriptor in enumerate(descriptors)}
        pcnt_idx = headers.index(vc.TOTAL_TIME)
        descriptor_idx = headers.index(vc.DESCRIPTOR)
        time_function_list = [np.array([0, 0]) for _ in range(len(descriptors))]

        for line in data:
            if line and line[descriptor_idx] in descriptor_pool:
                time_function_list[descriptor_pool[line[descriptor_idx]]] = \
                    np.array([line[pcnt_idx], line[descriptor_idx]])

        return self._generate_percentages(np.asarray(time_function_list))

    def process_function_names(self, function_names):
        return [utils.extract_constructor(name) or utils.extract_method(name) or name for name in function_names]

    def _generate_percentages(self, time_function_list):
        return np.round(time_function_list[:, 0].astype(np.float64) /
                        np.sum(time_function_list[:, 0].astype(np.float64)) * 100, decimals=1)

    def _generate_gradient(self, percentages):
        print('Generating gradient')
        gradient = list(range(100, 0, -int(100 / len(percentages))))[:len(percentages)]
        return [x / 100.0 for x in gradient]

    def _reverse_entries(self, sizes, lines):
        sizes.reverse()

        for pcnt, fn, grad in lines:
            pcnt.reverse()
