from hawk.data_stats.base_types import ColumnStat
from hawk.data_stats.column.general import PercentageMissingValues
from hawk.data_stats.column.categorical import NumOfCategories, Mode
from hawk.data_stats.column.numeric import (
    Min, Max, Mean, Median, StandardDeviation, Skewness, Kurtosis
)
import pandas as pd


STAT_COLUMN_GENERAL = {
    'percentage_missing_values': PercentageMissingValues
}

STAT_COLUMN_CATEGORICAL = {
    'num_of_categories': NumOfCategories,
    'mode': Mode
}

STAT_COLUMN_NUMERIC = {
    'min': Min,
    'max': Max,
    'mean': Mean,
    'median': Median,
    'std': StandardDeviation,
    'skewness': Skewness,
    'kurtosis': Kurtosis
}


def create_column_stat(name: str, column: pd.Series) -> ColumnStat:
    merged_mapping = STAT_COLUMN_GENERAL | STAT_COLUMN_NUMERIC | STAT_COLUMN_CATEGORICAL
    stat = merged_mapping.get(name, None)
    if not stat:
        raise ValueError(f'Stat with name {name} is not implemented.')
    return stat(column) # type: ignore
