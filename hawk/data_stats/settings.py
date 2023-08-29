from typing import Optional
from dataclasses import dataclass


@dataclass
class DataProfileSettings:
    """Class for defining settings for the generation process"""
    exclude_columns : Optional[list[str]]
    exclude_stats: Optional[list[str]]
