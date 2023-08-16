"""
This module contains the base class for column metrics
and functions to create general column metrics. The function name
corresponds to the name of the metric.
"""
from hawk.data_stats.stat_types import ColumnMetric
from hawk.data_stats.stat_calculators.base import StatsCalculator
import pandas as pd

    
class PercentageMissingValues(StatsCalculator):
    def calculate(column: pd.Series, column_name: str) -> ColumnMetric:
        return ColumnMetric(column=column_name, value=column.isna().sum() / column.size)


class PercentageDuplicates(StatsCalculator): 
    def calculate(column: pd.Series, column_name: str) -> ColumnMetric:
        return ColumnMetric(column=column_name, value=column.duplicated().sum() / column.size)
    

# Outliers: Percentage, Number, 
