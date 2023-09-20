from datetime import datetime
from uuid import uuid4
import pandas as pd

from hawk.data_stats.data_profile import DataProfile


class PipelineStage:
    def __init__(
        self, 
        descriptor: str,
        start_time: datetime,
        end_time: datetime,
        input_data: None | pd.DataFrame,
        output_data: None | pd.DataFrame
    ):
        self.descriptor = descriptor
        self.start_time = start_time
        self.end_time = end_time
        self.input_data = input_data
        self.output_data = output_data

    def as_dict(self):
        return {
            'descriptor': self.descriptor,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'input_data': self.get_input_data_profile().as_dict() 
                            if self.input_data is not None else {},
            'output_data': self.get_output_data_profile().as_dict() 
                            if self.output_data is not None else {}
        }
    
    def get_input_data_profile(self) -> None | DataProfile:
        if self.input_data is not None:
            return DataProfile(self.input_data)
        return None

    def get_output_data_profile(self) -> None | DataProfile:
        if self.output_data is not None:
            return DataProfile(self.output_data)
        return None


class PipelineRun:
    def __init__(self):
        self.run_id = str(uuid4())
        self.stages: list[PipelineStage] = []

    def add_stage(self, stage: PipelineStage) -> None:
        self.stages.append(stage)
