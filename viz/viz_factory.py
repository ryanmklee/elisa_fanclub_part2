import numpy as np

from viz.builder.bar_chart_builder import BarChart
from libs import utils

TOTAL_TIME = "tottime"
DESCRIPTOR = "filename:lineno(function)"

class VizFactory:
    FACTORY = {
        "horizontal_bar": BarChart
    }

    def render_viz(self, chart_type, headers, n_sizes, iteration_data):

        # withdraw first iteration to form backbone for processed_lines
        # then add each pcnt to the corresponding backbone entry for each extra iteration
        baseline_data = iteration_data[0]
        percentages, fn_names, fn_descriptors = self.extract_base_functions(baseline_data)
        gradient = self._generate_gradient(percentages)
        processed_lines = [([pcnt], fn, grad) for pcnt, fn, grad in
                           zip(percentages, fn_names, gradient)]

        for idx in range(1, len(iteration_data)):
            line_percentages = self.extract_iteration_percentages(iteration_data[idx], headers, fn_descriptors)
            for i, pcnt in enumerate(line_percentages):
                processed_lines[i][0].append(pcnt)

        builder = self.FACTORY[chart_type](processed_lines, n_sizes)
        builder.render()

    # returns 3-tuple with relevant functions we want to analyze
    # list of percentages, list of processed function names, list of their raw names for later iterations
    def extract_base_functions(self, data):
        print('Filtering data for visualization')
        lines = [x for x in data if x != []]
        np_lines = list(map(lambda line: np.array(line), lines))
        np_lines = list(filter(lambda line: float(line[1]) > 0, np_lines))
        time_function_list = np.array(list(map(lambda line: np.take(line, [1, 5]), np_lines)))
        percentages = self._generate_percentages(time_function_list)
        function_names = self.process_function_names(time_function_list[:, 1])

        return percentages, function_names, time_function_list[:, 1]

    # separate function to generate percentages for subsequent iterations beyond the first
    # because our extractor function excludes lines with runtime = 0
    # this is incorrect behavior for other iterations as we are still interested in them
    # the line itself may be absent, which is why times_function_list has placeholder np.arrays
    def extract_iteration_percentages(self, data, headers, descriptors):
        descriptor_pool = {descriptor: idx for idx, descriptor in enumerate(descriptors)}
        pcnt_idx = headers.index(TOTAL_TIME)
        descriptor_idx = headers.index(DESCRIPTOR)
        time_function_list = [np.array([0, 0]) for _ in range(len(descriptors))]

        for line in data:
            if line and line[descriptor_idx] in descriptor_pool:
                time_function_list[descriptor_pool[line[descriptor_idx]]] = \
                    np.array([line[pcnt_idx], line[descriptor_idx]])

        return self._generate_percentages(np.asarray(time_function_list))

    def process_function_names(self, function_names):
        return [utils.extract_constructor(name) or utils.extract_method(name) for name in function_names]

    def _generate_percentages(self, time_function_list):
        return np.round(time_function_list[:, 0].astype(np.float64) /
                               np.sum(time_function_list[:, 0].astype(np.float64)) * 100, decimals=1)

    def _generate_gradient(self, percentages):
        print('Generating gradient')
        gradient = list(range(100, 0, -int(100 / len(percentages))))[:len(percentages)]
        return [x / 100.0 for x in gradient]

