import json
from os.path import abspath, dirname, join

import numpy
from pandas import DataFrame, read_csv
from sklearn.compose import ColumnTransformer
from sklearn.impute import KNNImputer, SimpleImputer

from hawk import Pipeline, log_data


class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, numpy.integer):
            return int(obj)
        elif isinstance(obj, numpy.floating):
            return float(obj)
        elif isinstance(obj, numpy.ndarray):
            return obj.tolist()
        else:
            return super(CustomEncoder, self).default(obj)


current_dir = dirname(abspath((__file__)))
df = read_csv(join(current_dir, "datasets", "netflix.csv"))

run = Pipeline(df)

@log_data(run, "deduplication")
def deduplicate(df: DataFrame) -> DataFrame:
    return df.drop_duplicates()


@log_data(run, "missing_value_imputation")
def impute_missing_values(df: DataFrame) -> DataFrame:
    knn_imputer = KNNImputer(n_neighbors=3, weights="uniform")
    simple_imputer = SimpleImputer(missing_values="Not Given", strategy="most_frequent")
    transformers = ColumnTransformer(
        transformers=[
            ("imputation_num_features", knn_imputer, ["release_year"]),
            ("imputation_cat_features", simple_imputer, 
             ["show_id", "type", "director", "country", "rating", "duration", "listed_in"])
        ],
        remainder="passthrough",
        verbose_feature_names_out=False
    ).set_output(transform="pandas")
    return transformers.fit_transform(df)

df.pipe(deduplicate) \
  .pipe(impute_missing_values)

diffs = {}
for step in run.preprocessing_steps:
    input_data_profile = run.get_data_profile_of_dataset(step["input"])
    output_data_profile = run.get_data_profile_of_dataset(step["output"])
    diffs[step["description"]] = input_data_profile.calculate_diff(output_data_profile)

with open("example_output/diff.json", "w", encoding="utf-8") as diff_file:
    json.dump(diffs, diff_file, cls=CustomEncoder, indent=4)
