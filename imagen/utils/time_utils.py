import datetime as dt


def generate_file_timestamp() -> str:
    current_timestamp = dt.datetime.now(dt.UTC)
    return current_timestamp.strftime("%Y%m%d_%H%M%S")
