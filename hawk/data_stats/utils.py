from hawk.data_stats.column.factory import (
    STAT_COLUMN_CATEGORICAL, 
    STAT_COLUMN_GENERAL, 
    STAT_COLUMN_NUMERIC, 
    create_column_stat
)
from hawk.data_stats.correlation import CramersV, PearsonCorrelation
from hawk.exceptions import HawkException
from hawk.data_stats.base_types import ColumnStat, CorrelationStat, DataType, Column

from hashlib import sha256
from itertools import combinations

import pandas as pd
from pandas.util import hash_pandas_object

THRESHOLD_SIGNIFICANCE_CRAMERSV = 0.3
THRESHOLD_PVALUE_PEARSON = 0.05
THRESHOLD_USER_DEFINED_SIGNIFICANCE_PEARSON = 0.3


def generate_hash(dataset: pd.DataFrame) -> str:
    if isinstance(dataset, pd.DataFrame):
        return sha256(hash_pandas_object(dataset).values).hexdigest() # type: ignore
    else:
        raise HawkException(f'Input type "{type(dataset)}" not supported.')  


def create_column_descriptions(dataset: pd.DataFrame) -> list[Column]:
    column_descriptions = []
    for column_name in dataset:
        dtype = infer_dtype(dataset[column_name])
        column_descriptions.append(
            Column(name=str(column_name), 
                   dtype=dtype, 
                   stats=generate_stats_for_column(dataset[column_name], dtype=dtype)
            )
        )
    return column_descriptions


def infer_dtype(column: pd.Series) -> DataType:
    if column.dtype == 'int64' or column.dtype == 'float64':
        return DataType.NUMERIC
    elif column.dtype == 'datetime64':
        return DataType.DATETIME
    elif column.dtype == 'bool':
        return DataType.BOOLEAN
    else: 
        return DataType.CATEGORICAL


def generate_stats_for_column(column: pd.Series, dtype: DataType) -> list[ColumnStat]:
    stats = []
    for stat in STAT_COLUMN_GENERAL:
        stats.append(create_column_stat(stat, column))
    if dtype == DataType.NUMERIC:
        for stat in STAT_COLUMN_NUMERIC:
            stats.append(create_column_stat(stat, column))
    elif dtype == DataType.CATEGORICAL:
        for stat in STAT_COLUMN_CATEGORICAL:
            stats.append(create_column_stat(stat, column))
    else:
        pass
    return stats


def create_correlations(
    dataset: pd.DataFrame, 
    numeric_columns: list[str], 
    categorical_columns: list[str]
) -> list[CorrelationStat]:
    correlations: list[CorrelationStat] = []
    numeric_column_pairs = combinations(numeric_columns, 2)
    categorical_column_pairs = combinations(categorical_columns, 2)
    for column1, column2 in numeric_column_pairs:
        pearson = PearsonCorrelation(columns=(dataset[column1], dataset[column2]))
        # pearson.value[0] is the actual coefficient and pearson.value[1] is the pvalue
        if (abs(pearson.value[0]) >= THRESHOLD_USER_DEFINED_SIGNIFICANCE_PEARSON and 
                pearson.value[1] <= THRESHOLD_PVALUE_PEARSON):
                correlations.append(pearson)
    for column1, column2 in categorical_column_pairs:
        cramers_v = CramersV((dataset[column1], dataset[column2]))
        if cramers_v.value > THRESHOLD_SIGNIFICANCE_CRAMERSV:
            correlations.append(cramers_v)
    return correlations


def get_columns_of_type(
    input: list[Column], 
    dtype: DataType,
    names_only: bool = True
) -> list[Column] | list[str]:
    filtered_list = list(filter(lambda column: column.dtype == dtype, input))
    if names_only:
        return [column.name for column in filtered_list]
    return filtered_list
