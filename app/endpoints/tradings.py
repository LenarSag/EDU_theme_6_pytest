from typing import Annotated

from fastapi import Depends, APIRouter
from fastapi_filter import FilterDepends
from fastapi_pagination import Page, Params
from sqlalchemy.ext.asyncio import AsyncSession


from app.crud.trades_repository import (
    get_dynamics,
    get_last_trading_dates,
    get_trading_results,
)
from app.database.sql_database import get_session
from app.filters.spimex_filter import (
    TradingResultsDynamicsFilter,
    TradingResultsFilter,
    TradingResultsLastDatesFilter,
)
from app.models.user import User
from app.schemas.spimex import Trading
from app.security.authentication import get_current_user


tradesrouter = APIRouter()


@tradesrouter.get("/get-last-trading-dates", response_model=Page[Trading])
async def get_last_tradings(
    trades_filter: Annotated[
        TradingResultsLastDatesFilter, FilterDepends(TradingResultsLastDatesFilter)
    ],
    params: Annotated[Params, Depends()],
    session: Annotated[AsyncSession, Depends(get_session)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    return await get_last_trading_dates(session, trades_filter, params)


@tradesrouter.get("/get-dynamics", response_model=Page[Trading])
async def get_period_tradings(
    trades_filter: Annotated[
        TradingResultsDynamicsFilter, FilterDepends(TradingResultsDynamicsFilter)
    ],
    params: Annotated[Params, Depends()],
    session: Annotated[AsyncSession, Depends(get_session)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    return await get_dynamics(session, trades_filter, params)


@tradesrouter.get("/get-trading-results", response_model=Page[Trading])
async def get_tradings(
    trades_filter: Annotated[TradingResultsFilter, FilterDepends(TradingResultsFilter)],
    params: Annotated[Params, Depends()],
    session: Annotated[AsyncSession, Depends(get_session)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    return await get_trading_results(session, trades_filter, params)
