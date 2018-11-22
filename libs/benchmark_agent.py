import os


import pandas as pd
from sklearn.neighbors import KNeighborsClassifier


class BenchmarkAgent:
    def run_before(self, size=100):
        def load_csv_as_np_array(filename):
            return pd.read_csv(os.path.join('datasets', filename)).values

        self.volcano_test_X = load_csv_as_np_array('test_images.csv')[:size, :]
        self.volcano_test_y = load_csv_as_np_array('test_labels.csv')[1:size + 1, :1].flatten()

        volcano_train_X = load_csv_as_np_array('train_images.csv')[:size, :]
        volcano_train_y = load_csv_as_np_array('train_labels.csv')[1:size + 1, :1].flatten()
        self.model = KNeighborsClassifier().fit(volcano_train_X, volcano_train_y)

    def run_profile(self):
        def model_predict(X, model):
            return model.predict(X)

        model_predict(self.volcano_test_X, self.model)

    def run_after(self):
        pass

