from hawk import log_data, PipelineRun, send_pipeline_run_to_server

import pandas


pr = PipelineRun()

@log_data(pr, "ingestion")
def read_data(filename: str) -> pandas.DataFrame | None:
    try:
        df = pandas.read_csv(filename)
        return df
    except FileNotFoundError:
        print("Please enter a valid file")
        return None
    

contract_info = read_data("./datasets/contract_info.csv")
customer_info = read_data("./datasets/customer_info.csv")

merged_data = contract_info.join(other=customer_info, on="customer_id")
pr.add_processing_step("merging", [contract_info, customer_info], merged_data)


