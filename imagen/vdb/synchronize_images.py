from imagen.config import cfg
from imagen.vdb.lancedb_persistence import tbl


def cleanup_image_folder() -> None:
    """Remove images from the folder that are not in the database."""
    for file in cfg.image_path.glob("*"):
        res = tbl.search().where(f"image_name = '{file.name}'", prefilter=True).to_list()
        if len(res) == 0:
            print(f"Cannot find {file.name}")
            file.unlink()


def cleanup_db(limit: int = 1000) -> None:
    """Remove entries from the database that are not in the folder."""
    res = tbl.search().limit(limit).to_list()
    files = {f.name for f in list(cfg.image_path.glob("*"))}
    for row in res:
        image_name = row["image_name"]
        if image_name not in files:
            print(f"Image {image_name} not available in folder.")
            tbl.delete(where=f"image_name = '{image_name}'")


def syncronize_db(limit: int = 1000) -> None:
    """Synchronize the database with the image folder."""
    cleanup_image_folder()
    cleanup_db(limit)
