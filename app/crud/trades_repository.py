import json
from fastapi_pagination import Page, Params
from fastapi_pagination.ext.sqlalchemy import paginate
from redis import Redis
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.filters.spimex_filter import (
    TradingResultsDynamicsFilter,
    TradingResultsFilter,
    TradingResultsLastDatesFilter,
)
from app.models.spimex import TradingResults
from app.schemas.spimex import Trading


async def get_last_trading_dates(
    session: AsyncSession, trades_filter: TradingResultsLastDatesFilter, params: Params
):
    max_date_subquery = select(func.max(TradingResults.date)).scalar_subquery()
    if trades_filter.last_days and trades_filter.last_days != 0:
        query = select(TradingResults).where(
            TradingResults.date >= (max_date_subquery - trades_filter.last_days)
        )
    else:
        query = select(TradingResults)

    query = trades_filter.sort(query)

    return await paginate(session, query, params)


async def get_trading_dates_redis(redis: Redis, key: str):
    trades = await redis.get(f"trades:{key}")
    if trades:
        return trades
    return None


async def set_trading_data_to_redis(
    redis: Redis, key: str, data: dict, unix_timestamp: int
) -> None:
    await redis.set(f"trades:{key}", data, ex=unix_timestamp)


async def get_dynamics(
    session: AsyncSession, trades_filter: TradingResultsDynamicsFilter, params: Params
):
    query = select(TradingResults)

    if trades_filter.start_date:
        query = query.filter(TradingResults.date >= trades_filter.start_date)
        trades_filter.start_date = None
    if trades_filter.end_date:
        query = query.filter(TradingResults.date <= trades_filter.end_date)
        trades_filter.end_date = None

    query = trades_filter.filter(query)
    query = trades_filter.sort(query)

    return await paginate(session, query, params)


async def get_trading_results(
    session: AsyncSession, trades_filter: TradingResultsFilter, params: Params
):
    query = select(TradingResults)
    query = trades_filter.filter(query)
    query = trades_filter.sort(query)

    return await paginate(session, query, params)
