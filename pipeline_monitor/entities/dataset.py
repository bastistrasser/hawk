import pandas as pd
from pandas.util import hash_pandas_object
from typing import Union
from pipeline_monitor.exceptions import PipelineMonitorException
from pipeline_monitor.entities.data_profile import DataProfile


class Dataset:
    def __init__(self, dataset:Union(pd.DataFrame, list[dict])):
        self.id = self._calculate_id(dataset)
        self.schema = self._get_schema(dataset)
        self.profile = self._get_dataset_profile(dataset)

    def _calculate_id(dataset:Union(pd.DataFrame, list[dict])) -> int:
        if isinstance(dataset, pd.DataFrame):
            return hash_pandas_object(dataset)
        elif isinstance(dataset, list):
            return hash(tuple(dataset))
        else:
            raise PipelineMonitorException(f'Input type "{type(dataset)}" not supported.')

    def _get_schema(dataset:Union(pd.DataFrame, list[dict])) -> dict:
        if isinstance(dataset, pd.DataFrame):
            return {{ column_name: dtype } for column_name, dtype in zip(dataset.columns, dataset.dtypes)}
        elif isinstance(dataset, list):
            return {{ key: type(value) } for key, value in dataset[0]}
        else:
            raise PipelineMonitorException(f'Input type "{type(dataset)}" not supported.')

    def _get_dataset_profile(dataset:Union(pd.DataFrame, list[dict])) -> DataProfile:
        if isinstance(dataset, pd.DataFrame):
            pass
        elif isinstance(dataset, list):
            pass
        else:
            raise PipelineMonitorException(f'Input type "{type(dataset)}" not supported.')
