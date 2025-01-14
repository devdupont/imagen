from typing import TYPE_CHECKING, Any

import pandas as pd

if TYPE_CHECKING:
    from pyarrow.lib import Schema

from imagen.vdb.imagedb_schema import (
    FIELD_CREATE_TIMESTAMP,
    FIELD_IMAGE_DESCRIPTION,
    FIELD_IMAGE_NAME,
    FIELD_UPDATE_TIMESTAMP,
)
from imagen.vdb.lancedb_persistence import tbl

INFO_FIELDS = [
    FIELD_IMAGE_NAME,
    FIELD_IMAGE_DESCRIPTION,
    FIELD_CREATE_TIMESTAMP,
    FIELD_UPDATE_TIMESTAMP,
]


def basic_info() -> tuple[int, list[str]]:
    rows = tbl.count_rows()
    column_names = tbl.schema.names
    return rows, column_names


def col_info() -> list[tuple[str, Any]]:
    schema: Schema = tbl.schema
    return list(zip(schema.names, schema.types, strict=False))


def get_data() -> pd.DataFrame:
    # Limit -1 fetches all records
    df: pd.DataFrame = tbl.search().limit(-1).select(INFO_FIELDS).to_pandas()
    return df


if __name__ == "__main__":
    info = col_info()
    for i in info:
        print(i[0], i[1], type(i[1]))
    data = get_data()
    print(data.shape)
