from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from db.models import Trade, User, Market
from db.database import get_db
from models.schema import TradeCreateModel, TradeResponseModel, FastAPIResponseWrapper
from api.domain.trade_domain import create_trade_response


TRADE_ROUTES = APIRouter()

def trade_validations(trade: TradeCreateModel, user: User | None, market: Market | None):
    validate_user_and_market(user, market)
    validate_trade_option(trade, market)
    validate_user_balance(user, trade)

def validate_user_and_market(user: User | None, market: Market | None):
    if not user or not market:
        raise HTTPException(status_code=404, detail="User or Market not found")

def validate_trade_option(trade: TradeCreateModel, market: Market):
    if trade.option not in market.options:
        raise HTTPException(status_code=400, detail="Invalid option for this market")

def validate_user_balance(user: User, trade: TradeCreateModel):
    if user.balance < trade.amount:
        raise HTTPException(status_code=400, detail="Insufficient balance")

@TRADE_ROUTES.post("/trades", response_model=FastAPIResponseWrapper)
def create_trade(trade: TradeCreateModel, db: Session = Depends(get_db)) -> Trade:
    response, data = create_trade_response(trade, db)
    return FastAPIResponseWrapper(response=response, data=data)
