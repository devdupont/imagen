from typing import TYPE_CHECKING, Any

import pandas as pd

if TYPE_CHECKING:
    from pyarrow.lib import Schema

from imagen.model.image import FIELD
from imagen.vdb.lancedb_persistence import TBL


def basic_info() -> tuple[int, list[str]]:
    rows = TBL.count_rows()
    column_names = TBL.schema.names
    return rows, column_names


def col_info() -> list[tuple[str, Any]]:
    schema: Schema = TBL.schema
    return list(zip(schema.names, schema.types, strict=False))


def get_data() -> pd.DataFrame:
    # Limit -1 fetches all records
    df: pd.DataFrame = TBL.search().limit(-1).select(FIELD.info).to_pandas()
    return df


if __name__ == "__main__":
    info = col_info()
    for i in info:
        print(i[0], i[1], type(i[1]))
    data = get_data()
    print(data.shape)
