import pandas
import numpy

# General stats 
def percentage_missing_values(column: pandas.Series) -> float:
    return column.isna().sum() / column.size


# Stats for categorical features
def num_of_categories(column: pandas.Series) -> int:
    return column.unique().size


def mode(column: pandas.Series) -> str: 
    return column.mode(dropna=True)[0]


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


def histogram(column: pandas.Series) -> dict:
    hist = {}
    try:
        bins, edges = numpy.histogram(column)
        hist['bins'] = bins.tolist() 
        hist['edges'] = edges.tolist()
    except:
        print(f'Generation of histogram was not possible for column {column.name}')
    return hist


STAT_COLUMN_GENERAL = {
    'missing_values': percentage_missing_values
}

STAT_COLUMN_NUMERIC = {
    'min': min,
    'max': max,
    'mean': mean,
    'median': median,
    'std': std,
    'skewness': skewness,
    'kurtosis': kurtosis,
    'histogram': histogram
}

STAT_COLUMN_CATEGORICAL = {
    'num_of_categories': num_of_categories,
    'mode': mode
}
