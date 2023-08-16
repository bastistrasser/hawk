from hawk.data_stats.stat_types import Metric, Histogram
from hawk.data_stats.stat_calculators.base import StatsCalculator
from hawk.exceptions import PipelineMonitorException
from hawk.settings import GenerationSettings

import pandas as pd
from pandas.util import hash_pandas_object


class DataProfile:
    def __init__(self, dataset: pd.DataFrame, settings: GenerationSettings):
        self._id = self._generate_id(dataset)
        self._metrics = self._generate_metrics(dataset=dataset)
        self._histograms = self._generate_histograms(dataset=dataset)

    def _get_stat_calculators_from_settings() -> list[StatsCalculator]:
        pass

    def _generate_id(self, dataset: pd.DataFrame) -> int:
        if isinstance(dataset, pd.DataFrame):
            return hash_pandas_object(dataset)
        else:
            raise PipelineMonitorException(f'Input type "{type(dataset)}" not supported.')

    def _generate_metrics(self, dataset: pd.DataFrame) -> list[Metric]:
        pass

    def _generate_histograms(self, dataset: pd.DataFrame) -> list[Histogram]:
        pass
