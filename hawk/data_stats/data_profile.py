from hawk.data_stats.base_types import ColumnStat, CorrelationStat
from hawk.exceptions import HawkException
from hawk.data_stats.column.factory import ( 
    create_column_stat, 
    STAT_COLUMN_GENERAL,
    STAT_COLUMN_CATEGORICAL,
    STAT_COLUMN_NUMERIC
)

from dataclasses import dataclass
from hashlib import sha256
from enum import Enum

import pandas as pd
from pandas.util import hash_pandas_object


class DataType(Enum):
    NUMERIC = 1
    CATEGORICAL = 2
    DATETIME = 3
    BOOLEAN = 4


@dataclass
class Column:
    name: str
    dtype: DataType
    stats: list[ColumnStat]

    def __repr__(self) -> str:
        result = f'Name: {self.name} \nType: {self.dtype.name} \n'
        for stat in self.stats:
            result += f'{stat} \n'
        return result


class DataProfile:
    def __init__(self, dataset: pd.DataFrame):
        self.hash = generate_hash(dataset)
        self.rows = len(dataset.index)
        self.columns = create_column_descriptions(dataset)
        self.correlations = create_correlations(dataset)
    
    def __repr__(self) -> str:
        result = f'Hash: {self.hash} \nRows: {self.rows} \n'
        result += '--- Columns --- \n'
        for column in self.columns:
            result += f'{column} \n'
        if self.correlations:
            for correlation in self.correlations:
                result += f'{correlation} \n' 
        return result


def generate_hash(dataset: pd.DataFrame) -> str:
    if isinstance(dataset, pd.DataFrame):
        return sha256(hash_pandas_object(dataset).values).hexdigest()
    else:
        raise HawkException(f'Input type "{type(dataset)}" not supported.')  


def create_column_descriptions(dataset: pd.DataFrame) -> list[Column]:
    column_descriptions = []
    for column_name in dataset:
        dtype = infer_dtype(dataset[column_name])
        column_descriptions.append(
            Column(name=column_name, 
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


def create_correlations(dataset: pd.DataFrame) -> list[CorrelationStat]:
    pass
