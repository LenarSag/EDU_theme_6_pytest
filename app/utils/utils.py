from datetime import datetime, time, timedelta
import threading
import hashlib


from fastapi_filter.contrib.sqlalchemy import Filter
from fastapi_pagination import Params

from config import REDIS_EXP_HOUR, REDIS_EXP_MIN


def calculate_timestamp() -> int:
    print(f"Running calculate_timestamp in thread: {threading.get_ident()}")
    now = datetime.now()
    reset_time = datetime.combine(now.date(), time(REDIS_EXP_HOUR, REDIS_EXP_MIN))
    if reset_time <= now:
        reset_time += timedelta(days=1)
    unix_timestamp = int(reset_time.timestamp())

    return unix_timestamp


def hash_query_params(filter: Filter, params: Params) -> str:
    return hashlib.md5(
        f"{filter.model_dump()}-{params.model_dump()}".encode()
    ).hexdigest()
