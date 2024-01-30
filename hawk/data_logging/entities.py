from uuid import uuid4

import pandas

from hawk.data_profiling.data_profile import DataProfile


class Pipeline:
    def __init__(self, input_data: pandas.DataFrame | None = None):
        self.run_id = str(uuid4())
        self.datasets: list[dict] = []
        if input_data is not None:
            self.add_dataset(input_data)
        self.preprocessing_steps: list[dict] = []

    def add_dataset(self, dataset: pandas.DataFrame) -> int:
        new_dataset = {
            "id": len(self.datasets) + 1,
            "raw": dataset,
            "data_profile": DataProfile(dataset)
        }
        self.datasets.append(new_dataset)
        return new_dataset["id"] # type: ignore

    def get_data_profile_of_dataset(self, dataset_id: int) -> DataProfile | None:
        for dataset in self.datasets:
            if dataset["id"] == dataset_id:
                return dataset["data_profile"]
        return None

    def search_datasets(self, dataset_to_compare: pandas.DataFrame) -> str | None:
        if not self.datasets:
            return None
        try:    
            dataset = next(filter(
                lambda dataset: dataset["raw"].equals(dataset_to_compare), 
                self.datasets
            ))
            return dataset["id"]
        except (StopIteration, ValueError):
            return None

    def add_preprocessing_step(self, 
                              description: str, 
                              input_data: pandas.DataFrame, 
                              output_data: pandas.DataFrame) -> dict:
        input_id = self.search_datasets(input_data) 
        output_id = self.search_datasets(output_data)
        new_preprocessing_step = {
            "description": description,
            "input": input_id if input_id else self.add_dataset(input_data),
            "output": output_id if output_id else self.add_dataset(output_data)
        } 
        self.preprocessing_steps.append(new_preprocessing_step)
        return new_preprocessing_step
