import os
from jinja2 import Environment, FileSystemLoader

from hawk.monitoring.entities import Pipeline
from hawk.data_stats.data_profile import DataProfile
from hawk.data_stats.base_types import DataType
from hawk.visualization.utils import get_column_data_for_view, generate_image_from_file

current_path = os.path.dirname(__file__)
env = Environment(loader=FileSystemLoader(os.path.join(current_path, 'templates')))


def generate_workflow_overview(preprocessing_steps: list[dict]) -> str:
    dataset_template = env.get_template("dataset.html")
    preprocessing_step_template = env.get_template("preprocessing_step.html")
    dataset_image = generate_image_from_file(os.path.join(current_path, "assets", "dataset.png"))
    preprocessing_step_image = generate_image_from_file(os.path.join(current_path, "assets", "preprocessing_step.png"))
    overview = ""
    for index, step in enumerate(preprocessing_steps):
        if index < len(preprocessing_steps) - 1:
            overview += dataset_template.render(dataset_id=step["input"], image=dataset_image)
            overview += preprocessing_step_template.render(description=step["description"], image=preprocessing_step_image)
        else:
            overview += dataset_template.render(dataset_id=step["input"], image=dataset_image)
            overview += preprocessing_step_template.render(description=step["description"], image=preprocessing_step_image)
            overview += dataset_template.render(dataset_id=step["output"], image=dataset_image)
    return overview


def generate_column_information(dataset_id: str, data_profile: DataProfile):
    numeric_columns, categorical_columns, other_columns = [], [], []
    for column in data_profile.columns:
        if column.dtype == DataType.NUMERIC:
            numeric_columns.append(column)
        elif column.dtype == DataType.CATEGORICAL:
            categorical_columns.append(column)
        else:
            other_columns.append(column)
    numeric_headers, numeric_column_data = get_column_data_for_view(numeric_columns)
    categorical_headers, categorical_column_data = get_column_data_for_view(categorical_columns)
    other_headers, other_column_data = get_column_data_for_view(other_columns)
    template = env.get_template('column_information.html')
    return template.render(column_type='Numeric', headers=numeric_headers, columns=numeric_column_data) + \
           template.render(column_type='Categorical', headers=categorical_headers, columns=categorical_column_data) + \
           template.render(column_type='Other', headers=other_headers, columns=other_column_data)


def generate_comparison(pipeline: Pipeline):
    pass
