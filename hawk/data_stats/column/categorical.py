from hawk.data_stats.base_types import ColumnStat
import pandas as pd


class NumOfCategories(ColumnStat):
    def __init__(self, column: pd.Series):
        self._column = column
        self._value: int | None = None

    @property
    def value(self) -> int:
        if self._value is None:
            self._value = self._column.unique().size
        return self._value
        

class Mode(ColumnStat):
    def __init__(self, column: pd.Series):
        self._column = column
        self._value: str | None = None

    @property
    def value(self) -> str:
        if self._value is None:
            self._value = self._column.mode(dropna=True)[0]
        return self._value
