from hawk.data_stats.base_types import ColumnStat
import pandas as pd


class Min(ColumnStat):
    def __init__(self, column: pd.Series):
        self._column = column
        self._value: float | None = None

    @property
    def value(self) -> float:
        if self._value is None:
            self._value = self._column.min()
        return self._value
    

class Max(ColumnStat):
    def __init__(self, column: pd.Series):
        self._column = column
        self._value: float | None = None

    @property
    def value(self) -> float:
        if self._value is None:
            self._value = self._column.max()
        return self._value


class Mean(ColumnStat):
    def __init__(self, column: pd.Series):
        self._column = column
        self._value: float | None = None

    @property
    def value(self) -> float:
        if self._value is None:
            self._value = self._column.mean()
        return self._value


class Median(ColumnStat):
    def __init__(self, column: pd.Series):
        self._column = column
        self._value: float | None = None

    @property
    def value(self) -> float:
        if self._value is None:
            self._value = self._column.median()
        return self._value


class StandardDeviation(ColumnStat):
    def __init__(self, column: pd.Series):
        self._column = column
        self._value: float | None = None

    @property
    def value(self) -> float:
        if self._value is None:
            self._value = self._column.std()
        return self._value


class Skewness(ColumnStat):
    def __init__(self, column: pd.Series):
        self._column = column
        self._value: float | None = None

    @property
    def value(self) -> float:
        if self._value is None:
            self._value = self._column.skew() # type: ignore
        return self._value # type: ignore


class Kurtosis(ColumnStat):
    def __init__(self, column: pd.Series):
        self._column = column
        self._value: float | None = None

    @property
    def value(self) -> float:
        if self._value is None:
            self._value = self._column.kurtosis() # type: ignore
        return self._value # type: ignore
