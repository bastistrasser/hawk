from hawk.data_stats.base_types import CorrelationStat
from scipy.stats import pearsonr, chi2_contingency # type: ignore
import pandas as pd
import numpy as np


class PearsonCorrelation(CorrelationStat):
    def __init__(self, columns: tuple[pd.Series, pd.Series]):
        self._columns = columns
        self._value: tuple[float, float] | None = None

    @property
    def columns(self) -> tuple[pd.Series, pd.Series]:
        return self._columns
    
    @property
    def value(self) -> tuple[float, float]:
        if self._value is None:
            self._columns[0].fillna(0, inplace=True)
            self._columns[1].fillna(1, inplace=True)
            result = pearsonr(self._columns[0], self._columns[1])
            self._value = result.statistic, result.pvalue
        return self._value
    
class CramersV(CorrelationStat):
    def __init__(self, columns: tuple[pd.Series, pd.Series]):
        self._columns = columns
        self._value: float | None = None

    @property
    def columns(self) -> tuple[pd.Series, pd.Series]:
        return self._columns

    @property
    def value(self) -> float:
        if self._value is None:
            array = pd.crosstab(self._columns[0], self._columns[1]).to_numpy()
            chi2 = chi2_contingency(array).statistic
            phi2 = chi2 / array.sum()
            rows, columns = array.shape
            self._value = np.sqrt(phi2 / min(columns-1, rows-1))
        return self._value
