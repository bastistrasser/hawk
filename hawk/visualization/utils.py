import numpy
from PIL import Image
import base64
import io


from hawk.data_stats.base_types import Column


def get_column_data_for_view(columns: list[Column], exclude_stats: list[str] = ["histogram"], float_precision: int = 2):
    def format_property(property):
        if isinstance(property, float) or isinstance(property, numpy.floating):
            return f"{property:.{float_precision}f}"
        else:
            return property
    headers, metadata_per_column = [], []
    if columns:
        headers = ["name"] + [stat for stat in columns[0].stats if not stat in exclude_stats]
        for column in columns:
            metadata = [column.name]
            for stat in column.stats:
                if stat not in exclude_stats:
                    metadata.append(format_property(column.stats.get(stat)))
            metadata_per_column.append(metadata)
    return headers, metadata_per_column


def generate_image_from_file(filename):
    img = Image.open(filename)
    img_data = io.BytesIO()
    img.save(img_data, "png")
    encoded_img_data = base64.b64encode(img_data.getvalue())
    return encoded_img_data.decode("utf-8")