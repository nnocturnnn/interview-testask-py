from fastapi import APIRouter, Depends, Query
from httpx import AsyncClient
from datetime import datetime
from typing import List

from app.api import models, enums
from app.api.schemas import QueryParams, HistoricalPricesResponse

router = APIRouter()
client = AsyncClient()

@router.post("/download/{company}", response_model=List[HistoricalPricesResponse])
async def download(company: enums.Companies, query_params: QueryParams = Depends()) -> List[HistoricalPricesResponse]:
    url = f"https://query1.finance.yahoo.com/v7/finance/download/{company}"
    query_params = query_params.dict()
    query_params['period1'] = query_params['period2'].strftime("%s") if query_params['period1'] else 0
    response = await _get(url=url, params=query_params, company=company)
    return response


@router.get("/", response_model=List[HistoricalPricesResponse])
async def get_historical_prices(company: enums.Companies = Query(..., description="Company name")) -> List[HistoricalPricesResponse]:
    response = await models.HistoricalPrices.filter(company__name=company.value)
    return response


async def _get(url: str, params: dict, company: enums.Companies):
    async with AsyncClient() as client:
        response = await client.get(url, params=params)
        result = []
        if response.status_code == 200:
            company_id, _ = await models.Company.get_or_create(name=company.value)
            for resp in response.iter_lines():
                r = resp.strip().split(",")
                if "Date" not in r:
                    data = {"open": r[1], "high": r[2], "low": r[3], "close": r[4],
                            "adj_close": r[5], "volume": r[6]}
                    res, _ = await models.HistoricalPrices.get_or_create(
                        date=datetime.strptime(r[0], "%Y-%m-%d"), company=company_id, **data)
                    result.append(dict(res))
        return result




