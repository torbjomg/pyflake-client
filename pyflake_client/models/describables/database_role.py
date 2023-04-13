"""role"""
from dataclasses import dataclass

from dacite import Config

from pyflake_client.models.describables.snowflake_describable_interface import (
    ISnowflakeDescribable,
)
from pyflake_client.models.describables.snowflake_grant_principal import (
    ISnowflakeGrantPrincipal,
)
from pyflake_client.models.enums.role_type import RoleType

@dataclass(frozen=True)
class DatabaseRole(ISnowflakeDescribable, ISnowflakeGrantPrincipal):
    """Role"""

    name: str
    db_name: str

    def get_describe_statement(self) -> str:
        """get_describe_statement"""
        return f"SHOW {RoleType.DATABASE_ROLE.pluralize()} LIKE '{self.name}' IN DATABASE {self.db_name};".upper()

    def is_procedure(self) -> bool:
        """is_procedure"""
        return False

    def get_dacite_config(self) -> Config:
        return None

    @staticmethod
    def get_snowflake_type() -> str:
        """get_snowflake_type"""
        return "DATABASE ROLE"