import cProfile
import pstats
import io
import os

import numpy as np
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier


# testing stuff out for now


def load_csv_as_np_array(filename):
    return pd.read_csv(os.path.join('datasets', filename)).values


def model_predict(X, model):
    return model.predict(X)


def convert_profiler_to_lists(profiler):
    lines = []
    s = io.StringIO()
    stats = pstats.Stats(profiler, stream=s).sort_stats('tottime')
    stats.print_stats()

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

    return headers, lines


if __name__ == '__main__':
    profiler = cProfile.Profile()

    volcano_test_X = load_csv_as_np_array('test_images.csv')[:500, :]
    volcano_test_y = load_csv_as_np_array('test_labels.csv')[1:501, :1].flatten()

    volcano_train_X = load_csv_as_np_array('train_images.csv')[:500, :]
    volcano_train_y = load_csv_as_np_array('train_labels.csv')[1:501, :1].flatten()
    model = KNeighborsClassifier().fit(volcano_test_X, volcano_test_y)

    profiler.enable()
    model_predict(volcano_test_X, model)
    profiler.disable()

    headers, lines = convert_profiler_to_lists(profiler)
    print(lines)
    print(headers)

