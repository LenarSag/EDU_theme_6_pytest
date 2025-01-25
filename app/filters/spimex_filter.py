from datetime import date
from typing import Optional

from fastapi_filter.contrib.sqlalchemy import Filter

from app.models.spimex import TradingResults


class TradingResultsLastDatesFilter(Filter):
    last_days: Optional[int] = None

    order_by: list[str] = ["date"]

    class Constants(Filter.Constants):
        model = TradingResults


class TradingResultsDynamicsFilter(Filter):
    oil_id: Optional[str] = None
    delivery_basis_id: Optional[str] = None
    delivery_type_id: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None

    order_by: list[str] = ["date"]

    class Constants(Filter.Constants):
        model = TradingResults


class TradingResultsFilter(Filter):
    oil_id: Optional[str] = None
    delivery_basis_id: Optional[str] = None
    delivery_type_id: Optional[str] = None

    order_by: list[str] = ["date"]

    class Constants(Filter.Constants):
        model = TradingResults
