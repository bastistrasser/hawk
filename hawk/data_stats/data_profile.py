from hawk.data_stats.base_types import DataType
from hawk.data_stats.utils import (
    generate_hash,
    create_column_descriptions,
    create_correlations, 
    get_columns_of_type
)
import pandas as pd


class DataProfile:
    def __init__(self, dataset: pd.DataFrame):
        self.hash = generate_hash(dataset)
        self.rows = len(dataset.index)
        self.num_columns = len(dataset.columns)
        self.columns = create_column_descriptions(dataset)
        self.correlations = create_correlations(
            dataset, 
            numeric_columns=get_columns_of_type(self.columns, 
                                                DataType.NUMERIC,
                                                names_only=True), # type: ignore
            categorical_columns=get_columns_of_type(self.columns,
                                                    DataType.CATEGORICAL,
                                                    names_only=True) # type: ignore
        )
    
    def __repr__(self) -> str:
        result = f'Hash: {self.hash} \nRows: {self.rows} \n'
        result += '--- Columns --- \n'
        for column in self.columns:
            result += f'{column} \n'
        if self.correlations:
            for correlation in self.correlations:
                result += f'{correlation} \n' 
        return result
