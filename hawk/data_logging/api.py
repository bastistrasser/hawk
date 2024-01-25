import pandas

from hawk.data_logging.entities import Pipeline


def log_data(run: Pipeline, preprocessing_description: str):
    def wrapper(func):
        def with_data_logging(*args, **kwargs):
            input_data = None
            output_data = None
            for arg in args:
                if isinstance(arg, pandas.DataFrame):
                    input_data = arg
                    break
            if input_data is None:
                for kwarg in kwargs:    
                    if isinstance(kwarg, pandas.DataFrame):
                        input_data = kwarg
            result = func(*args, **kwargs)
            if isinstance(result, pandas.DataFrame):
                output_data = result
            if output_data is not None:
                run.add_preprocessing_step(
                    preprocessing_description, input_data, output_data
                )
            return result
        return with_data_logging
    return wrapper
