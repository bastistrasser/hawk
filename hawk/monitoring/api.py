from datetime import datetime
import pandas as pd

from hawk.monitoring.entities import PipelineRun, PipelineStage


def log_data(run: PipelineRun, pipeline_stage_descriptor: str):
    def wrapper(func):
        def with_data_logging(*args, **kwargs):
            start_time = datetime.now()
            input_data = None
            output_data = None
            for arg in args:
                if isinstance(arg, pd.DataFrame):
                    input_data = arg
            if input_data is None:
                for key in kwargs:
                    if isinstance(kwargs[key], pd.DataFrame):
                        input_data = kwargs[key]
            result = func(*args, **kwargs)
            if isinstance(result, pd.DataFrame):
                output_data = result
            if input_data is not None or output_data is not None:
                run.add_stage(
                    PipelineStage(
                        descriptor=pipeline_stage_descriptor,
                        start_time=start_time,
                        end_time=datetime.now(),
                        input_data=input_data,
                        output_data=output_data
                    )
                )
            return result
        return with_data_logging
    return wrapper
