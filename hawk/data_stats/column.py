import numpy
import pandas


# General stats 
def missing_rate(column: pandas.Series) -> float:
    return column.isna().sum() / column.size


# Stats for categorical features
def num_of_categories(column: pandas.Series) -> int:
    return column.unique().size


def mode(column: pandas.Series) -> str: 
    return column.mode(dropna=True)[0]


def frequency_distribution(column: pandas.Series) -> dict:
    return column.value_counts().to_dict()


# Stats for numeric features
def min(column: pandas.Series) -> float:
    return column.min()


def max(column: pandas.Series) -> float:
    return column.max()


def mean(column: pandas.Series) -> float:
    return column.mean()


def median(column: pandas.Series) -> float:
    return column.median()


def std(column: pandas.Series) -> float:
    return column.std()


def skewness(column: pandas.Series) -> float:
    return column.skew()


def kurtosis(column: pandas.Series) -> float:
    return column.kurtosis()


def mad(column: pandas.Series) -> float:
    return (column - column.median()).abs().median()


def histogram(column: pandas.Series) -> dict:
    hist = {}
    try:
        unique_values = column.dropna().unique()
        if len(unique_values) < 10:
            num_bins = len(unique_values)
        else:
            num_bins = 10 # TODO: research what is a good range
        bins, edges = numpy.histogram(column.dropna(), bins=num_bins)
        hist["bins"] = bins.tolist() 
        hist["edges"] = edges.tolist()
    except ValueError:
        print(f"Generation of histogram was not possible for column {column.name}")
    return hist


STAT_COLUMN_GENERAL = {
    "missing_rate": missing_rate
}

STAT_COLUMN_NUMERIC = {
    "min": min,
    "max": max,
    "mean": mean,
    "median": median,
    "std": std,
    "median_absolute_deviation": mad,
    "skewness": skewness,
    "kurtosis": kurtosis,
    "histogram": histogram,
}

STAT_COLUMN_CATEGORICAL = {
    "num_of_categories": num_of_categories,
    "mode": mode,
    "frequency_distribution": frequency_distribution
}
