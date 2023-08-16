import pandas as pd
from hawk.data_stats.stat_types import ColumnMetric
from hawk.data_stats.stat_calculators.base import StatsCalculator


# here: number of categories, quantiles (mode?)
class NumberOfCategories(StatsCalculator):
    def calculate(column: pd.Series, column_name: str) -> ColumnMetric:
        return ColumnMetric(column=column_name, result=float(column.unique().size))
    

class Mode(StatsCalculator):
    def calculate(column: pd.Series, column_name: str) -> ColumnMetric:
        mode = column.mode(dropna=True)[0]
        return ColumnMetric(column_name=column_name, result=mode)
