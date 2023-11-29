from hawk import PipelineRun, log_data
from pandas import DataFrame, read_csv
from sklearn.impute import KNNImputer, SimpleImputer
from sklearn.compose import ColumnTransformer
from os.path import join, dirname, abspath
import json

run = PipelineRun()

@log_data(run, 'ingestion')
def load_data(filename: str) -> DataFrame:
    return read_csv(filename)


@log_data(run, 'deduplication')
def deduplicate(df: DataFrame) -> DataFrame:
    return df.drop_duplicates()


@log_data(run, 'missing_value_imputation')
def impute_missing_values(df: DataFrame) -> DataFrame:
    knn_imputer = KNNImputer(n_neighbors=3, weights='uniform')
    simple_imputer = SimpleImputer(missing_values='Not Given', strategy='most_frequent')
    transformers = ColumnTransformer(
        transformers=[
            ('imputation_num_features', knn_imputer, ['release_year']),
            ('imputation_cat_features', simple_imputer, ['show_id', 'type', 'director', 'country', 'rating', 'duration', 'listed_in'])
        ],
        remainder='passthrough',
        verbose_feature_names_out=False
    ).set_output(transform='pandas')
    return transformers.fit_transform(df)

current_dir = dirname(abspath((__file__)))
load_data(join(current_dir, 'datasets', 'netflix.csv')) \
    .pipe(deduplicate) \
    .pipe(impute_missing_values)

for stage in run.stages:
    output_data_profile = stage.get_output_data_profile().as_dict()
    with open(f'{stage.descriptor}.json', 'w') as data_profile:
        data_profile.write(json.dumps(output_data_profile))
