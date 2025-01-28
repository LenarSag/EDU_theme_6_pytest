from datetime import datetime, time, timedelta
import hashlib

from fastapi_filter.contrib.sqlalchemy import Filter
from fastapi_pagination import Params


def calculate_timestamp() -> int:
    now = datetime.now()
    reset_time = datetime.combine(now.date(), time(14, 11))
    if reset_time <= now:
        reset_time += timedelta(days=1)
    unix_timestamp = int(reset_time.timestamp())

    return unix_timestamp


def hash_query_params(filter: Filter, params: Params):
    return hashlib.md5(
        f"{filter.model_dump()}-{params.model_dump()}".encode()
    ).hexdigest()
