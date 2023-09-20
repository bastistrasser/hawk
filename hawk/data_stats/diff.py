from hawk.data_stats.base_types import Column
from hawk.data_stats.data_profile import DataProfile
from dataclasses import dataclass


@dataclass
class ColumnDiff:
    pass


@dataclass
class Diff:
    num_row_difference: int
    removed_columns: list[str]
    added_columns: list[str]


def create_diff(previous: DataProfile, new: DataProfile) -> None | Diff:
    if previous.hash == new.hash:
        return None
    column_names_previous = [column.name for column in previous.columns]
    column_names_new = [column.name for column in new.columns]
    column_names_combined = set(column_names_previous + column_names_new)
    added_columns = list(set(column_names_new) - column_names_combined)
    removed_columns = list(set(column_names_previous) - column_names_combined)
    for column_name in column_names_combined:
        column_previous = next(filter(lambda column: column.name == column_name, previous.columns))
        column_new = next(filter(lambda column: column.name == column_name, new.columns))
        compare_column_versions(column_previous, column_new)
    return Diff(
        num_row_difference=(new.num_rows - previous.num_rows),
        removed_columns=removed_columns,
        added_columns=added_columns
    )


def compare_column_versions(column1: Column, column2: Column) -> ColumnDiff:
    if column1.dtype != column2.dtype:
          pass
