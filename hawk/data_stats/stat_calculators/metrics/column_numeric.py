from hawk.data_stats.stat_types import ColumnMetric
from hawk.data_stats.stat_calculators.base import StatsCalculator
import pandas as pd


class Minimum(StatsCalculator):
    def calculate(column: pd.Series, column_name: str) -> ColumnMetric:
        return ColumnMetric(column=column_name, result=column.min(numeric_only=True))


class Maximum(StatsCalculator):
    def calculate(column: pd.Series, column_name: str) -> ColumnMetric:
        return ColumnMetric(column=column_name, result=column.max(numeric_only=True))


class Average(StatsCalculator):
    def calculate(column: pd.Series, column_name: str) -> ColumnMetric:
        return ColumnMetric(column=column_name, result=column.mean(numeric_only=True))


class StandardDeviation(StatsCalculator):
    def calculate(column: pd.Series, column_name: str) -> ColumnMetric:
        return ColumnMetric(column=column_name, result=column.std(numeric_only=True))


class Skewness(StatsCalculator):
    def calculate(column: pd.Series, column_name: str) -> ColumnMetric:
        return ColumnMetric(column=column_name, result=column.skew(numeric_only=True))


class Kurtosis(StatsCalculator):
    def calculate(column: pd.Series, column_name: str) -> ColumnMetric:
        return ColumnMetric(column=column_name, value=column.kurtosis(numeric_only=True))
