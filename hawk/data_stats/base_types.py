from abc import ABC, abstractmethod
import pandas as pd


class Histogram:
    def __init__(self, bins: pd.Series, values: pd.Series):
        self._bins = bins
        self._values = values
    
    @property
    def bins(self) -> pd.Series:
        return self._bins
    
    def values(self) -> pd.Series:
        return self._values


class ColumnStat(ABC):
    @property
    @abstractmethod
    def value(self) -> int | float | str | Histogram:
        raise NotImplementedError

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}: {self.value}'


class CorrelationStat(ABC):
    @property
    @abstractmethod
    def columns(self) -> tuple[str, str]:
        raise NotImplementedError
    
    @property
    @abstractmethod
    def value(self) -> float:
        raise NotImplementedError