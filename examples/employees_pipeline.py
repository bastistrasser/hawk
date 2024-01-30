import json
from os.path import abspath, dirname, join

from hawk import Pipeline, log_data

import numpy
import pandas
from sklearn.impute import KNNImputer, SimpleImputer
from sklearn.compose import ColumnTransformer


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
df = pandas.read_csv(
    join(current_dir, "datasets", "employees_v1.csv"), 
    parse_dates = ["entry_date"], 
    date_format = "%d.%m.%Y"
)

pipeline = Pipeline(df)

@log_data(pipeline, "missing_value_imputation")
def impute_missing_values(df: pandas.DataFrame, num_columns, cat_columns) -> pandas.DataFrame:
    knn_imputer = KNNImputer(n_neighbors=3, weights="uniform")
    simple_imputer = SimpleImputer(strategy="most_frequent")
    col_transformer = ColumnTransformer(
        transformers=[
            ("num_column_imputer", knn_imputer, num_columns),
            ("cat_column_imputer", simple_imputer, cat_columns)
        ],
        remainder="passthrough",
        verbose_feature_names_out=False
    ).set_output(transform="pandas")
    return col_transformer.fit_transform(df)


@log_data(pipeline, "one_hot_encoding")
def one_hot_encoding(df: pandas.DataFrame, columns) -> pandas.DataFrame:
    return pandas.get_dummies(df, columns=columns)


df.pipe(impute_missing_values, num_columns=["age", "salary"], cat_columns=["gender"]) \
  .pipe(one_hot_encoding, columns=["gender", "department"])

diffs = {}
for preprocessing_step in pipeline.preprocessing_steps:
    input_data_profile = pipeline.get_data_profile_of_dataset(dataset_id=preprocessing_step["input"])
    output_data_profile = pipeline.get_data_profile_of_dataset(dataset_id=preprocessing_step["output"])
    output_data_profile.to_json(f"example_output/output_{preprocessing_step['description']}.json")
    diffs[preprocessing_step["description"]] = input_data_profile.calculate_diff(output_data_profile)

with open("example_output/diff.json", "w", encoding="utf-8") as diff_file:
    json.dump(diffs, diff_file, cls=CustomEncoder, indent=4)
