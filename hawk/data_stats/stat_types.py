"""This module contains 
"""

from abc import ABC, abstractmethod
from typing import Union


class Metric(ABC):
    """Base class for all metrics
    """
    @property
    @abstractmethod 
    def result(self) -> Union(str, float):
        pass


class ColumnMetric(Metric):
    """Class for metrics referring to a single column
    """
    def __init__(self, column_name: str, result: Union(str, float)):
        self._column_name = column_name
        self._result = result

    @property
    def column_name(self) -> str:
        return self._column_name

    @property
    def result(self) -> Union(str, float):
        return self._result


class CorrelationMetric(Metric):
    """Class for metrics referring correlations
    """
    def __init__(self, column_pair: tuple(str, str), result: Union(str, float)):
        self._column_pair = column_pair
        self._result = result

    @property
    def column_pair(self) -> (str, str):
        return self._column_pair

    @property
    def result(self) -> float:
        return self._result


class Histogram():
    def __init__(self):
        pass
