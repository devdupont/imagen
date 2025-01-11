from pathlib import Path


def unlink_file(tmp_path: Path) -> None:
    if tmp_path is not None:
        # try:
        tmp_path.unlink()
        # except Exception as exc:
        #     logger.exception(f"Failed to delete {tmp_path}: {exc}")
