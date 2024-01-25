import json
from hashlib import sha256
from itertools import combinations, product
from typing import Any, Self

import numpy
import pandas
from pandas.util import hash_pandas_object

from hawk.data_stats.base_types import Column, CorrelationStat, FeatureType
from hawk.data_stats.column import (STAT_COLUMN_CATEGORICAL,
                                    STAT_COLUMN_GENERAL, STAT_COLUMN_NUMERIC)
from hawk.data_stats.correlation import CramersV, PearsonCorrelation
from hawk.exceptions import HawkException

THRESHOLD_CRAMERSV = 0.3
MAX_PVALUE_PEARSON = 0.05
THRESHOLD_PEARSON = 0.3


def generate_hash(dataset: pandas.DataFrame) -> str:
    if isinstance(dataset, pandas.DataFrame):
        return sha256(hash_pandas_object(dataset).values).hexdigest() # type: ignore
    else:
        raise HawkException(f"Input type '{type(dataset)}' not supported.")  


def create_column_descriptions(dataset: pandas.DataFrame) -> list[Column]:
    column_descriptions = []
    for column_name in dataset.sort_index(axis=1):
        feature_type = infer_feature_type(dataset[column_name])
        column_descriptions.append(
            Column(name=str(column_name), 
                   feature_type=feature_type,
                   internal_dtype=str(dataset[column_name].dtype),
                   stats=generate_stats_for_column(dataset[column_name], 
                                                   feature_type=feature_type)
            )
        )
    return column_descriptions


def infer_feature_type(column: pandas.Series) -> FeatureType:
    if column.dtype == "int64" or column.dtype == "float64":
        return FeatureType.NUMERIC
    elif numpy.issubdtype(column, numpy.datetime64): # type: ignore
        return FeatureType.DATETIME
    elif column.dtype == "bool":
        return FeatureType.BOOLEAN
    elif column.dtype == "object":

        return FeatureType.CATEGORICAL
    else:
        return FeatureType.NOT_IMPLEMENTED


def generate_stats_for_column(column: pandas.Series, feature_type: FeatureType) -> dict:
    stats = {}
    for stat_name, stat_func in STAT_COLUMN_GENERAL.items():
        stats[stat_name] = stat_func(column)
    if feature_type == FeatureType.NUMERIC:
        for stat_name, stat_func in STAT_COLUMN_NUMERIC.items(): # type: ignore
            stats[stat_name] = stat_func(column)
    elif feature_type == FeatureType.CATEGORICAL:
        for stat_name, stat_func in STAT_COLUMN_CATEGORICAL.items(): # type: ignore
            stats[stat_name] = stat_func(column)
    else:
        pass
    return stats


def create_correlations(dataset: pandas.DataFrame, 
                        numeric_columns: list[str], 
                        categorical_columns: list[str],
                        max_pvalue_pearson: float,
                        threshold_pearson: float, 
                        threshold_cramers_v: float) -> list[CorrelationStat]:
    correlations: list[CorrelationStat] = []
    numeric_column_pairs = combinations(numeric_columns, 2)
    categorical_column_pairs = combinations(categorical_columns, 2)
    for column1, column2 in numeric_column_pairs:
        pearson = PearsonCorrelation(columns=(dataset[column1], dataset[column2]))
        # pearson.value[0] is the Pearson coefficient and pearson.value[1] is the pvalue
        if (abs(pearson.value[0]) >= threshold_pearson and 
                pearson.value[1] <= max_pvalue_pearson):
                correlations.append(pearson)
    for column1, column2 in categorical_column_pairs:
        cramers_v = CramersV((dataset[column1], dataset[column2]))
        if cramers_v.value > threshold_cramers_v:
            correlations.append(cramers_v)
    return correlations


def get_columns_of_type(
    input: list[Column], 
    feature_type: FeatureType,
    names_only: bool = True
) -> list[Column] | list[str]:
    filtered_list = list(
        filter(lambda column: column.feature_type == feature_type, input)
    )
    if names_only:
        return [column.name for column in filtered_list]
    return filtered_list


def get_column_diffs(column_1: Column, column_2: Column) -> dict:
    column_diffs = {}
    stat_names = column_1.stats.keys()
    for stat_name in stat_names:
        stat_old = column_1.stats.get(stat_name)
        stat_new = column_2.stats.get(stat_name)
        stat_diff = 0
        if stat_old and stat_new and type(stat_old) not in [str, dict]:
            stat_diff = stat_new - stat_old
        if stat_diff != 0:
             column_diffs[stat_name] = stat_diff
    return column_diffs


def get_correlation_diff(correlation_1: CorrelationStat, 
                         correlation_2: CorrelationStat) -> dict:
    if set(correlation_1.columns) == set(correlation_2.columns):
        if isinstance(correlation_1, PearsonCorrelation):
            correlation_diff = tuple(
                numpy.subtract(correlation_2.value[0], correlation_1.value[1]) # type: ignore
            )
            if correlation_diff != (0, 0):
                return {
                    "type": correlation_1.__class__.__name__,
                    "column_1": correlation_1.columns[0],
                    "column_2": correlation_1.columns[1],
                    "diff_value": correlation_diff[0],
                    "diff_pvalue": correlation_diff[1]
                }
        else:
            correlation_diff = correlation_2.value - correlation_1.value # type: ignore
            if correlation_diff != 0:
                return {
                    "type": correlation_1.__class__.__name__,
                    "column_1": correlation_1.columns[0],
                    "column_2": correlation_1.columns[1],
                    "diff": correlation_diff
                }                            
    return {}


class NumpyEncoder(json.JSONEncoder):
    def default(self, obj: Any) -> Any:
        if isinstance(obj, numpy.integer):
            return int(obj)
        elif isinstance(obj, numpy.floating):
            return float(obj)
        elif isinstance(obj, numpy.ndarray):
            return obj.tolist()
        else:
            return super(NumpyEncoder, self).default(obj)


class DataProfile:
    def __init__(self, dataset: pandas.DataFrame):
        self.hash = generate_hash(dataset)
        self.num_rows = len(dataset.index)
        self.num_columns = len(dataset.columns)
        self.columns = create_column_descriptions(dataset)
        self.correlations = create_correlations(
            dataset, 
            numeric_columns=get_columns_of_type(input=self.columns, 
                                                feature_type=FeatureType.NUMERIC,
                                                names_only=True), # type: ignore
            categorical_columns=get_columns_of_type(input=self.columns,
                                                    feature_type=FeatureType.CATEGORICAL,
                                                    names_only=True), # type: ignore
            max_pvalue_pearson=MAX_PVALUE_PEARSON,
            threshold_pearson=THRESHOLD_PEARSON,
            threshold_cramers_v=THRESHOLD_CRAMERSV 
        )

    def __repr__(self) -> str:
        result = f"Hash: {self.hash} \nNumber of rows: {self.num_rows}"
        result += f"\nNumber of columns: {self.num_columns}\n\n"
        result += "--- Columns ---\n"
        for column in self.columns:
            result += f"{column} \n"
        if self.correlations:
            result += "--- Correlations ---\n"
            for correlation in self.correlations:
                result += f"{correlation} \n" 
        return result

    def get_schema_information(self) -> list[dict]:
        return [
            { "name": column.name, "type": column.internal_dtype } 
            for column in self.columns
        ]

    def as_dict(self) -> dict:
        return {
            "hash": self.hash,
            "num_rows": self.num_rows,
            "num_columns": self.num_columns,
            "columns": list(map(lambda column: column.as_dict(), self.columns)),
            "correlations": 
                list(map(lambda correlation: correlation.as_dict(), self.correlations))
        }

    def calculate_diff(self, other: Self) -> dict:
        diff: dict[str, Any] = {}
        if self.hash == other.hash:
            return diff
        diff["columns"] = {}
        for column, column_other in zip(self.columns, other.columns):
            diff["columns"][column.name] = get_column_diffs(column, column_other)
        
        diff["correlations"] = [] # type: ignore
        for correlation, correlation_other in product(
            self.correlations, other.correlations
        ):
            correlation_diff = get_correlation_diff(correlation, correlation_other)
            if correlation_diff:
                diff["correlations"].append(correlation_diff) # type: ignore
        return diff

    def to_json(self, filename: str):
        with open(filename, "w") as output_file:
            json.dump(self.as_dict(), output_file, cls=NumpyEncoder, indent=4)
