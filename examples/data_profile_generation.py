import pandas as pd
from os.path import join, dirname, abspath
import json
import numpy

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
data = pd.read_csv(join(current_dir, 'datasets', 'hotel_bookings.csv'))
data = data.astype({'is_canceled': 'bool', 'is_repeated_guest': 'bool'})
data_profile = DataProfile(dataset=data)
with open('test.json', 'w') as test_file:
    json.dump(data_profile.as_dict(), test_file, cls=NumpyEncoder)
