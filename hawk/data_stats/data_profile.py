from hawk.data_stats.column import STAT_COLUMN_GENERAL, STAT_COLUMN_NUMERIC, STAT_COLUMN_CATEGORICAL
from hawk.data_stats.correlation import CramersV, PearsonCorrelation
from hawk.exceptions import HawkException
from hawk.data_stats.base_types import CorrelationStat, DataType, Column

from hashlib import sha256
from itertools import combinations
import pandas
from pandas.util import hash_pandas_object


THRESHOLD_CRAMERSV = 0.3
MAX_PVALUE_PEARSON = 0.05
THRESHOLD_PEARSON = 0.3


def generate_hash(dataset: pandas.DataFrame) -> str:
    if isinstance(dataset, pandas.DataFrame):
        return sha256(hash_pandas_object(dataset).values).hexdigest() # type: ignore
    else:
        raise HawkException(f'Input type "{type(dataset)}" not supported.')  


def create_column_descriptions(dataset: pandas.DataFrame) -> list[Column]:
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


def infer_dtype(column: pandas.Series) -> DataType:
    if column.dtype == 'int64' or column.dtype == 'float64':
        return DataType.NUMERIC
    elif column.dtype == 'datetime64':
        return DataType.DATETIME
    elif column.dtype == 'bool':
        return DataType.BOOLEAN
    else: 
        return DataType.CATEGORICAL


def generate_stats_for_column(column: pandas.Series, dtype: DataType) -> dict:
    stats = {}
    for stat_name, stat_func in STAT_COLUMN_GENERAL.items():
        stats[stat_name] = stat_func(column)
    if dtype == DataType.NUMERIC:
        for stat_name, stat_func in STAT_COLUMN_NUMERIC.items():
            stats[stat_name] = stat_func(column)
    elif dtype == DataType.CATEGORICAL:
        for stat_name, stat_func in STAT_COLUMN_CATEGORICAL.items():
            stats[stat_name] = stat_func(column)
    else:
        pass
    return stats


def create_correlations(
    dataset: pandas.DataFrame, 
    numeric_columns: list[str], 
    categorical_columns: list[str],
    max_pvalue_pearson: float,
    threshold_pearson: float, 
    threshold_cramers_v: float
) -> list[CorrelationStat]:
    correlations: list[CorrelationStat] = []
    numeric_column_pairs = combinations(numeric_columns, 2)
    categorical_column_pairs = combinations(categorical_columns, 2)
    for column1, column2 in numeric_column_pairs:
        pearson = PearsonCorrelation(columns=(dataset[column1], dataset[column2]))
        # pearson.value[0] is the Pearson coefficient and pearson.value[1] is the pvalue
        if (abs(pearson.value[0]) >= threshold_pearson and 
                pearson.value[1] <= max_pvalue_pearson):
                correlations.append(pearson)
    for column1, column2 in categorical_column_pairs:
        cramers_v = CramersV((dataset[column1], dataset[column2]))
        if cramers_v.value > threshold_cramers_v:
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

class DataProfile:
    def __init__(self, dataset: pandas.DataFrame):
        self.hash = generate_hash(dataset)
        self.num_rows = len(dataset.index)
        self.num_columns = len(dataset.columns)
        self.columns = create_column_descriptions(dataset)
        self.correlations = create_correlations(
            dataset, 
            numeric_columns=get_columns_of_type(input=self.columns, 
                                                dtype=DataType.NUMERIC,
                                                names_only=True), # type: ignore
            categorical_columns=get_columns_of_type(input=self.columns,
                                                    dtype=DataType.CATEGORICAL,
                                                    names_only=True), # type: ignore
            max_pvalue_pearson=MAX_PVALUE_PEARSON,
            threshold_pearson=THRESHOLD_PEARSON,
            threshold_cramers_v=THRESHOLD_CRAMERSV 
        )

    def __repr__(self) -> str:
        result = f'Hash: {self.hash} \nNumber of rows: {self.num_rows}'
        result += f'\nNumber of columns: {self.num_columns}\n\n'
        result += '--- Columns ---\n'
        for column in self.columns:
            result += f'{column} \n'
        if self.correlations:
            result += '--- Correlations ---\n'
            for correlation in self.correlations:
                result += f'{correlation} \n' 
        return result

    def as_dict(self) -> dict:
        return {
            'hash': self.hash,
            'num_rows': self.num_rows,
            'num_columns': self.num_columns,
            'columns': list(map(lambda column: column.as_dict(), self.columns)),
            'correlations': 
                list(map(lambda correlation: correlation.as_dict(), self.correlations))
        }
