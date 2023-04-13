"""schema"""
from dataclasses import dataclass
from datetime import datetime
from typing import Union

from dacite import Config

from pyflake_client.models.describables.snowflake_describable_interface import (
    ISnowflakeDescribable,
)


@dataclass(frozen=True)
class Schema(ISnowflakeDescribable):
    """Schema"""

    name: str
    database_name: str
    owner: Union[str, None] = None
    comment: Union[str, None] = None
    retention_time: Union[int, None] = None
    created_on: Union[datetime, None] = None

    def get_describe_statement(self) -> str:
        """get_describe_statement"""
        return (
            f"SHOW SCHEMAS LIKE '{self.name}' IN DATABASE {self.database_name}".upper()
        )

    def is_procedure(self) -> bool:
        """is_procedure"""
        return False

    def get_dacite_config(self) -> Union[Config, None]:
        return None
