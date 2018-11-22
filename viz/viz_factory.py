import numpy as np

from viz.builder.bar_chart_builder import BarChart


class VizFactory:
    FACTORY = {
        "horizontal_bar": BarChart
    }

    def render_viz(self, chart_type, data):
        function_names, percentages = self.filter_data(data)
        gradient = self._generate_gradient(percentages)
        processed_lines = [(pcnt, fn, grad) for pcnt, fn, grad in
                           zip(percentages, function_names, gradient)]

        builder = self.FACTORY[chart_type](processed_lines)
        builder.render()

    def filter_data(self, data):
        print('Filtering data for visualization')
        lines = [x for x in data if x != []]
        np_lines = list(map(lambda line: np.array(line), lines))
        np_lines = list(filter(lambda line: float(line[1]) > 0, np_lines))
        time_function_list = np.array(list(map(lambda line: np.take(line, [1, 5]), np_lines)))
        percentages = np.round(time_function_list[:, 0].astype(np.float64) /
                                    np.sum(time_function_list[:, 0].astype(np.float64)) * 100, decimals=1)
        function_names = time_function_list[:, 1]

        return percentages, function_names

    def _generate_gradient(self, percentages):
        print('Generating gradient')
        gradient = list(range(100, 0, -int(100 / len(percentages))))[:len(percentages)]
        return [x / 100.0 for x in gradient]

