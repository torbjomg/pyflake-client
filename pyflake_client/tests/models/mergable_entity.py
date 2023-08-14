# -*- coding: utf-8 -*-
# pylint: disable=line-too-long
# pylint: disable=invalid-name
# pylint: disable=too-many-locals

from dataclasses import dataclass
from datetime import datetime
from typing import Union

from pyflake_client.models.assets.table_columns import (
    Bool,
    Identity,
    Integer,
    Timestamp,
    Varchar,
)
from pyflake_client.models.mergeables.snowflake_mergable_interface import (
    ISnowflakeMergable,
)

# --------------------------------------------------------
# --- Test dependencies
# --------------------------------------------------------

TABLE_NAME = "merge_table"
TABLE_COLUMN_DEFINITION = [
    Integer("id", identity=Identity(1, 1)),
    Varchar("the_primary_key", primary_key=True),
    Bool(name="enabled"),
    Timestamp(name="valid_from"),
    Timestamp(name="valid_to"),
]


@dataclass
class MergableEntity(ISnowflakeMergable):
    """MergableEntity"""

    def configure(self, db_name:str, schema_name:str, table_name: str):
        self._db_name = db_name
        self._schema_name = schema_name
        self._table_name = table_name

        return self

    the_primary_key: str
    enabled: Union[bool, None] = None
    valid_from: Union[datetime, None] = None
    valid_to: Union[datetime, None] = None
    id: Union[int, None] = None

    def merge_into_statement(self) -> str:
        """merge_into_statement"""
        now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f%z")
        return f"""
        merge into {self._db_name}.{self._schema_name}.{self._table_name} tar using
        (
            select
                '{self.the_primary_key}' THE_PRIMARY_KEY,
                '{self.enabled}' ENABLED,
                '{now}'::timestamp_ntz(2)  VALID_FROM,
                '9999-12-31 23:59:59.99' VALID_TO
            union all
            select
                s.the_primary_key,
                s.enabled,
                s.valid_from,
                '{now}'::timestamp_ntz(2) valid_to
            from {self._db_name}.{self._schema_name}.{self._table_name} s
            where
                s.THE_PRIMARY_KEY = '{self.the_primary_key}'
                and s.VALID_TO::date = '9999-12-31'
        )src on
            src.THE_PRIMARY_KEY = tar.THE_PRIMARY_KEY
            and src.VALID_FROM = tar.VALID_FROM
        WHEN MATCHED THEN UPDATE
            set tar.VALID_TO = '{now}'::timestamp_ntz(2)
        WHEN NOT MATCHED THEN INSERT (
            THE_PRIMARY_KEY,
            ENABLED,
            VALID_FROM,
            VALID_TO
        ) VALUES (
            src.THE_PRIMARY_KEY,
            src.ENABLED,
            src.VALID_FROM,
            src.VALID_TO
        );
        """

    def select_statement(self) -> str:
        """select_statement"""
        return f"""
        select
            *
        from {self._db_name}.{self._schema_name}.{self._table_name} s
        where s.the_primary_key = '{self.the_primary_key}' and valid_to::date = '9999-12-31'
        """
