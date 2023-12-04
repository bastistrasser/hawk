from jinja2 import Environment, FileSystemLoader
import os

from hawk.monitoring.entities import Pipeline
from hawk.visualization import html_generation as html_gen


def make_report(pipeline: Pipeline):
    overview = html_gen.generate_workflow_overview(pipeline.preprocessing_steps)
    column_information = ""
    for dataset in pipeline.datasets:
        column_information += html_gen.generate_column_information(dataset["id"], dataset["data_profile"])
    env = Environment(loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')))
    template = env.get_template('main.html')
    report = template.render(workflow_overview=overview, 
                             column_information=column_information)
    with open('report.html', mode='w') as report_file:
        report_file.write(report)
