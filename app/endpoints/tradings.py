import asyncio
import json
from typing import Annotated

from fastapi import Depends, APIRouter, Response
from fastapi_filter import FilterDepends
from fastapi_pagination import Page, Params
from redis import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.cache_repository import (
    get_trading_dates_redis,
    set_trading_data_to_redis,
)
from app.crud.trades_repository import (
    get_dynamics,
    get_last_trading_dates,
    get_trading_results,
)
from app.database.redis_db import get_redis
from app.database.sql_database import get_session
from app.filters.spimex_filter import (
    TradingResultsDynamicsFilter,
    TradingResultsFilter,
    TradingResultsLastDatesFilter,
)
from app.models.user import User
from app.schemas.spimex import Trading
from app.security.authentication import get_current_user
from app.utils.utils import calculate_timestamp, hash_query_params


tradesrouter = APIRouter()


def query_to_json(trades: Page[Trading]) -> str:
    items_dict = [
        Trading.model_dump(Trading.model_validate(item)) for item in trades.items
    ]
    data_dict = {
        "items": items_dict,
        "total": trades.total,
        "page": trades.page,
        "size": trades.size,
        "pages": trades.pages,
    }

    return json.dumps(
        data_dict,
        default=str,
        ensure_ascii=False,
    )


@tradesrouter.get("/get-last-trading-dates", response_class=Response)
async def get_last_tradings(
    trades_filter: Annotated[
        TradingResultsLastDatesFilter, FilterDepends(TradingResultsLastDatesFilter)
    ],
    params: Annotated[Params, Depends()],
    session: Annotated[AsyncSession, Depends(get_session)],
    redis: Annotated[Redis, Depends(get_redis)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    # hash filters and params to get cached data
    key = await asyncio.to_thread(hash_query_params, trades_filter, params)

    cached_trades = await get_trading_dates_redis(redis, key)
    if cached_trades:
        return Response(cached_trades)

    paginated_trades = await get_last_trading_dates(session, trades_filter, params)
    serialized_data = await asyncio.to_thread(query_to_json, paginated_trades)
    unix_timestamp = await asyncio.to_thread(calculate_timestamp)

    await set_trading_data_to_redis(redis, key, serialized_data, unix_timestamp)

    return Response(serialized_data)


@tradesrouter.get("/get-dynamics", response_class=Response)
async def get_period_tradings(
    trades_filter: Annotated[
        TradingResultsDynamicsFilter, FilterDepends(TradingResultsDynamicsFilter)
    ],
    params: Annotated[Params, Depends()],
    session: Annotated[AsyncSession, Depends(get_session)],
    redis: Annotated[Redis, Depends(get_redis)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    # hash filters and params to get cached data
    key = await asyncio.to_thread(hash_query_params, trades_filter, params)

    cached_trades = await get_trading_dates_redis(redis, key)
    if cached_trades:
        return Response(cached_trades)

    paginated_trades = await get_dynamics(session, trades_filter, params)
    serialized_data = await asyncio.to_thread(query_to_json, paginated_trades)
    unix_timestamp = await asyncio.to_thread(calculate_timestamp)

    await set_trading_data_to_redis(redis, key, serialized_data, unix_timestamp)

    return Response(serialized_data)


@tradesrouter.get("/get-trading-results", response_class=Response)
async def get_tradings(
    trades_filter: Annotated[TradingResultsFilter, FilterDepends(TradingResultsFilter)],
    params: Annotated[Params, Depends()],
    session: Annotated[AsyncSession, Depends(get_session)],
    redis: Annotated[Redis, Depends(get_redis)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    # hash filters and params to get cached data
    key = await asyncio.to_thread(hash_query_params, trades_filter, params)

    cached_trades = await get_trading_dates_redis(redis, key)
    if cached_trades:
        return Response(cached_trades)

    paginated_trades = await get_trading_results(session, trades_filter, params)
    serialized_data = await asyncio.to_thread(query_to_json, paginated_trades)
    unix_timestamp = await asyncio.to_thread(calculate_timestamp)

    await set_trading_data_to_redis(redis, key, serialized_data, unix_timestamp)

    return Response(serialized_data)
