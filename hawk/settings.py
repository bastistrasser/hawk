from hawk.data_stats.stat_types import Metric, Histogram
from typing import Self


class GenerationSettings:
    def __init__(self):
        self._metrics = list[Metric]
        self._histograms = list[Histogram]


    @classmethod
    def from_json_config(cls, filename: str) -> Self:
        pass
