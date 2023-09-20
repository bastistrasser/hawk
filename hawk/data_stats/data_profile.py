from hawk.data_stats.base_types import DataType
from hawk.data_stats.utils import (
    generate_hash,
    create_column_descriptions,
    create_correlations, 
    get_columns_of_type
)
import pandas as pd


THRESHOLD_CRAMERSV = 0.3
MAX_PVALUE_PEARSON = 0.05
THRESHOLD_PEARSON = 0.3


class DataProfile:
    def __init__(self, dataset: pd.DataFrame):
        self.hash = generate_hash(dataset)
        self.num_rows = len(dataset.index)
        self.num_columns = len(dataset.columns)
        self.columns = create_column_descriptions(dataset)
        self.correlations = create_correlations(
            dataset, 
            numeric_columns=get_columns_of_type(input=self.columns, 
                                                dtype=DataType.NUMERIC,
                                                names_only=True), # type: ignore
            categorical_columns=get_columns_of_type(input=self.columns,
                                                    dtype=DataType.CATEGORICAL,
                                                    names_only=True), # type: ignore
            max_pvalue_pearson=MAX_PVALUE_PEARSON,
            threshold_pearson=THRESHOLD_PEARSON,
            threshold_cramers_v=THRESHOLD_CRAMERSV 
        )

    def __repr__(self) -> str:
        result = f'Hash: {self.hash} \nNumber of rows: {self.num_rows}'
        result += f'\nNumber of columns: {self.num_columns}\n\n'
        result += '--- Columns ---\n'
        for column in self.columns:
            result += f'{column} \n'
        if self.correlations:
            result += '--- Correlations ---\n'
            for correlation in self.correlations:
                result += f'{correlation} \n' 
        return result

    def as_dict(self) -> dict:
        return {
            'hash': self.hash,
            'num_rows': self.num_rows,
            'num_columns': self.num_columns,
            'columns': list(map(lambda column: column.as_dict(), self.columns)),
            'correlations': 
                list(map(lambda correlation: correlation.as_dict(), self.correlations))
        }
