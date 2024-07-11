from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, validator


class QueryParams(BaseModel):
    period1: Optional[date]
    period2: Optional[date] = datetime.now().date()
    interval: Optional[str] = "1d"
    events: Optional[str] = "history"
    includeAdjustedClose: Optional[bool] = True


    @validator("period1", "period2", always=True)
    def validate_date(cls, v, values):

        if values.get("period1") and v:
            if v < values["period1"]:
                raise ValueError
        if isinstance(v, date):
            v = v.strftime("%s")
        return v


class HistoricalPricesResponse(BaseModel):
    id: int
    company_id: int
    date: date
    open: float
    high: float
    low: float
    close: float
    adj_close: float
    volume: float
