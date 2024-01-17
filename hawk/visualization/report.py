import os

from jinja2 import Environment, FileSystemLoader

from hawk.monitoring.entities import Pipeline
from hawk.visualization import html_generation as html_gen
from hawk.visualization.utils import (get_column_data_for_view,
                                      split_columns_by_type)


def make_report(pipeline: Pipeline):
    overview = html_gen.generate_workflow_overview(pipeline.preprocessing_steps)
    view_datasets = []
    for dataset in pipeline.datasets:
        view = {}
        view["id"] = dataset["id"]
        num_columns, cat_columns, other_columns = \
            split_columns_by_type(dataset["data_profile"].columns)
        view["columns_by_type"] = {
            "Numeric": get_column_data_for_view(num_columns) if num_columns else {},
            "Categorical": get_column_data_for_view(cat_columns) if cat_columns else {},
            "Other": get_column_data_for_view(other_columns) if other_columns else {}
        }
        view_datasets.append(view)
    env = Environment(
        loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), "templates"))
    )
    template = env.get_template("main.html")
    report = template.render(workflow_overview=overview, 
                             datasets=view_datasets,
                             preprocessing_steps=pipeline.preprocessing_steps)
    with open("report.html", mode="w") as report_file:
        report_file.write(report)
