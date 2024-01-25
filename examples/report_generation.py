from os.path import abspath, dirname, join

from pandas import DataFrame, read_csv
from sklearn.compose import ColumnTransformer
from sklearn.impute import KNNImputer, SimpleImputer

from hawk import Pipeline, log_data, make_report

current_dir = dirname(abspath((__file__)))
df = read_csv(join(current_dir, 'datasets', 'netflix.csv'))

run = Pipeline(df)

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

df.pipe(deduplicate) \
  .pipe(impute_missing_values)

report = make_report(run)
with open("report.html", mode="w", encoding="utf-8") as report_file:
    report_file.write(report)
