import pandas as pd
from hawk import DataProfile
from os.path import join, dirname, abspath


current_dir = dirname(abspath((__file__)))
data = pd.read_csv(join(current_dir, 'datasets', 'hotel_bookings.csv'))
data = data.astype({'is_canceled': 'bool', 'is_repeated_guest': 'bool'})
data_profile = DataProfile(dataset=data)
print(data_profile)
