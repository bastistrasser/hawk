from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
import pandas as pd


class DataType(str, Enum):
    NUMERIC = 'NUMERIC'
    CATEGORICAL = 'CATEGORICAL'
    DATETIME = 'DATETIME'
    BOOLEAN = 'BOOLEAN'


class CorrelationStat(ABC):
    @property
    @abstractmethod
    def columns(self) -> tuple[pd.Series, pd.Series]:
        raise NotImplementedError
    
    @property
    @abstractmethod
    def value(self) -> float | tuple[float, float]:
        raise NotImplementedError
    
    def __repr__(self) -> str:
        value_repr = self.value[0] if isinstance(self.value, tuple) else self.value
        return (
            f'{self.__class__.__name__}({self.columns[0].name} '
            f'and {self.columns[1].name}): {value_repr}'
        )

    def as_dict(self) -> dict:
        return {
            self.__class__.__name__: {
                'columns': list(map(lambda column: column.name, self.columns)),
                'value': self.value
            }
        }

@dataclass
class Column:
    name: str
    dtype: DataType
    stats: dict

    def __repr__(self) -> str:
        result = f'Name: {self.name} \nType: {self.dtype.name} \n'
        for stat in self.stats:
            result += f'{stat}: {self.stats[stat] } \n'
        return result

    def as_dict(self) -> dict:
        return {
            'name': self.name,
            'dtype': self.dtype,
            'stats': self.stats
        }
