import json
from os.path import abspath, dirname, join

import numpy
import pandas as pd

from hawk import DataProfile


class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, numpy.integer):
            return int(obj)
        elif isinstance(obj, numpy.floating):
            return float(obj)
        elif isinstance(obj, numpy.ndarray):
            return obj.tolist()
        else:
            return super(NumpyEncoder, self).default(obj)

current_dir = dirname(abspath((__file__)))
data = pd.read_csv(join(current_dir, 'datasets', 'employees_satisfaction.csv'))
data_profile = DataProfile(dataset=data)
data_profile.to_json('test.json')
