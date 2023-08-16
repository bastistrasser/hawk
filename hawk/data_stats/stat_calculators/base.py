from hawk.data_stats.stat_types import Metric, Histogram
from abc import ABC, abstractmethod
from typing import Any

class StatsCalculator(ABC):
    @abstractmethod
    @staticmethod
    def calculate(args: Any) -> Metric | Histogram:
        raise NotImplementedError
