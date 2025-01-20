from imagen.config import cfg
from imagen.model.image import FIELD
from imagen.vdb.lancedb_persistence import TBL


def cleanup_image_folder() -> None:
    """Remove images from the folder that are not in the database."""
    for file in cfg.image_path.glob("*"):
        res = TBL.search().where(f"{FIELD.name} = '{file.name}'", prefilter=True).to_list()
        if len(res) == 0:
            print(f"Cannot find {file.name}")
            file.unlink()


def cleanup_db(limit: int = 1000) -> None:
    """Remove entries from the database that are not in the folder."""
    res = TBL.search().limit(limit).to_list()
    files = {f.name for f in list(cfg.image_path.glob("*"))}
    for row in res:
        name = row[FIELD.name]
        if name not in files:
            print(f"Image {name} not available in folder.")
            TBL.delete(where=f"{FIELD.name} = '{name}'")


def syncronize_db(limit: int = 1000) -> None:
    """Synchronize the database with the image folder."""
    cleanup_image_folder()
    cleanup_db(limit)
