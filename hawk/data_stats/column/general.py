from hawk.data_stats.base_types import ColumnStat
import pandas as pd


class PercentageMissingValues(ColumnStat):
    def __init__(self, column: pd.Series):
        self._column = column
        self._value: float | None = None

    @property
    def value(self) -> float:
        if self._value is None:
            self._value = self._column.isna().sum() / self._column.size
        return self._value
