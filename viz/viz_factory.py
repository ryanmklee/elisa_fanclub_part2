import numpy as np

from viz.builder.bar_chart_builder import BarChart
from libs import utils


class VizFactory:
    FACTORY = {
        "horizontal_bar": BarChart
    }

    def render_viz(self, chart_type, n_sizes, iteration_data):

        # withdraw first iteration to form backbone for processed_lines
        # then add each pcnt to the corresponding backbone entry for each extra iteration
        baseline_data = iteration_data[0]
        percentages, function_names = self.filter_data(baseline_data)
        gradient = self._generate_gradient(percentages)
        processed_lines = [([pcnt], fn, grad) for pcnt, fn, grad in
                           zip(percentages, function_names, gradient)]

        for idx in range(1, len(iteration_data)):
            line_percentages, _ = self.filter_data(iteration_data[idx])
            # TODO: filter_data removes entries with pcnt = 0, this is an issue because the first iteration
            # TODO: might've had a non-zero pcnt entry, and removing this messes up bars later down
            # TODO: fix filter_data so that it adds 0 when we need the entry
            for i, pcnt in enumerate(line_percentages):
                processed_lines[i][0].append(pcnt)

        builder = self.FACTORY[chart_type](processed_lines, n_sizes)
        builder.render()

    def filter_data(self, data):
        print('Filtering data for visualization')
        lines = [x for x in data if x != []]
        np_lines = list(map(lambda line: np.array(line), lines))
        np_lines = list(filter(lambda line: float(line[1]) > 0, np_lines))
        time_function_list = np.array(list(map(lambda line: np.take(line, [1, 5]), np_lines)))
        percentages = np.round(time_function_list[:, 0].astype(np.float64) /
                                    np.sum(time_function_list[:, 0].astype(np.float64)) * 100, decimals=1)
        function_names = self.process_function_names(time_function_list[:, 1])

        return percentages, function_names

    def process_function_names(self, function_names):
        return [utils.extract_constructor(name) or utils.extract_method(name) for name in function_names]

    def _generate_gradient(self, percentages):
        print('Generating gradient')
        gradient = list(range(100, 0, -int(100 / len(percentages))))[:len(percentages)]
        return [x / 100.0 for x in gradient]

