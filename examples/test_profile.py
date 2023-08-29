from hawk import DataProfile
from sklearn.datasets import load_iris
import pandas as pd


data = load_iris()
df = pd.DataFrame(data.data, columns=data.feature_names)
profile = DataProfile(dataset=df)
