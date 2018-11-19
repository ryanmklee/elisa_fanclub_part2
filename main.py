import cProfile
import pstats
import io, os

import numpy as np
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier

# testing stuff out for now


def load_csv_as_np_array(filename):
    return pd.read_csv(os.path.join('datasets', filename)).values

def model_predict(X, model):
    return model.predict(X)

def convert_to_human_readable_form(profiler):
    pass

if __name__ == '__main__':
    profiler = cProfile.Profile()

    volcano_test_X = load_csv_as_np_array('test_images.csv')[:500,:]
    volcano_test_y = load_csv_as_np_array('test_labels.csv')[1:501,:1].flatten()

    volcano_train_X = load_csv_as_np_array('train_images.csv')[:500,:]
    volcano_train_y = load_csv_as_np_array('train_labels.csv')[1:501,:1].flatten()
    model = KNeighborsClassifier().fit(volcano_test_X, volcano_test_y)

    profiler.enable()
    model_predict(volcano_test_X, model)
    profiler.disable()

    s = io.StringIO()
    stats = pstats.Stats(profiler, stream=s).sort_stats('tottime')
    stats.print_stats()

    with open('test.txt', 'w+') as f:
        f.write(s.getvalue())
