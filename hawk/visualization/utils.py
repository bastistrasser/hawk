import base64
import io

import numpy
from PIL import Image

from hawk.data_profiling.base_types import Column, FeatureType


def get_column_data_for_view(
        columns: list[Column], 
        exclude_stats: list[str] = ["histogram", "frequency_distribution"], 
        float_precision: int = 2
):
    def format_property(property):
        if isinstance(property, float) or isinstance(property, numpy.floating):
            return f"{property:.{float_precision}f}"
        else:
            return property
    headers, metadata_per_column = [], []
    if columns:
        headers = ["name"] + \
            [stat for stat in columns[0].stats if stat not in exclude_stats]
        for column in columns:
            metadata = [column.name]
            for stat in column.stats:
                if stat not in exclude_stats:
                    metadata.append(format_property(column.stats.get(stat)))
            metadata_per_column.append(metadata)
    return {
        "headers": headers, 
        "metadata": metadata_per_column
    }


def generate_image_from_file(filename):
    img = Image.open(filename)
    img_data = io.BytesIO()
    img.save(img_data, "png")
    encoded_img_data = base64.b64encode(img_data.getvalue())
    return encoded_img_data.decode("utf-8")


def split_columns_by_type(columns: list[Column], exclude_columns: list[str] = []):
    numeric_columns, categorical_columns, other_columns = [], [], []
    for column in columns:
        if column.name in exclude_columns:
            continue
        if column.feature_type == FeatureType.NUMERIC:
            numeric_columns.append(column)
        elif column.feature_type == FeatureType.CATEGORICAL:
            categorical_columns.append(column)
        else:
            other_columns.append(column)
    return numeric_columns, categorical_columns, other_columns