import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from models.schema import MarketModel, MarketResponseModel, FastAPIResponseWrapper, ResponseModel
from sqlalchemy.orm import Session
from models.response import Http
from db.models import Market
from db.database import get_db

MARKETS_ROUTES = APIRouter()


@MARKETS_ROUTES.post("/markets", response_model=FastAPIResponseWrapper)
def create_market(market: MarketModel, db: Session = Depends(get_db)) -> Market:
    options: List[str] = market.options
    json_options: List[dict] = []
    for index, option in enumerate(options):
        json_options.append(
            {
                "id": index,
                "name": option.strip(),
                "votes": 0,
            }
        )
    new_market = Market(
        id=uuid.uuid4(),
        question=market.question,
        description=market.description,
        close_date=market.close_date,
        options=json_options,
        creator_id=market.creator_id,
    )
    db.add(new_market)
    db.commit()
    db.refresh(new_market)
    return FastAPIResponseWrapper(
        response=ResponseModel(status=Http.StatusOk, message="Market created successfully"),
        data=MarketResponseModel(
            id=str(new_market.id),
            question=new_market.question,
            description=new_market.description,
            close_date=new_market.close_date,
            options=new_market.options,
            creator_id=str(new_market.creator_id),
        )
    )


@MARKETS_ROUTES.get("/markets", response_model=FastAPIResponseWrapper)
def list_markets(db: Session = Depends(get_db)) -> list[Market]:
    markets = db.query(Market).all()
    return FastAPIResponseWrapper(
        response=ResponseModel(status=Http.StatusOk, message="Markets fetched successfully"),
        data=[
            MarketResponseModel(
                id=str(market.id),
                question=market.question,
                description=market.description,
                close_date=market.close_date,
                options=market.options,
                creator_id=str(market.creator_id),
            )
            for market in markets
        ]
    )


@MARKETS_ROUTES.get("/markets/{market_id}", response_model=FastAPIResponseWrapper)
def get_market(market_id: str, db: Session = Depends(get_db)) -> Market:
    market = db.query(Market).filter(Market.id == market_id).first()
    if not market:
        raise HTTPException(status_code=404, detail="Market not found")
    return FastAPIResponseWrapper(
        response=ResponseModel(status=Http.StatusOk, message="Market fetched successfully"),
        data=MarketResponseModel(
            id=str(market.id),
            question=market.question,
            description=market.description,
            close_date=market.close_date,
            options=market.options,
            creator_id=str(market.creator_id),
        )
    )
