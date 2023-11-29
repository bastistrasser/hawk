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
        output_data: pd.DataFrame
    ):
        self.descriptor = descriptor
        self.start_time = start_time
        self.end_time = end_time
        self.data_profile = DataProfile(output_data)

    def as_dict(self):
        return {
            'descriptor': self.descriptor,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'data_profile': self.data_profile
        }


class PipelineRun:
    def __init__(self):
        self.run_id = str(uuid4())
        self.stages: list[PipelineStage] = []

    def add_stage(self, stage: PipelineStage) -> None:
        self.stages.append(stage)
