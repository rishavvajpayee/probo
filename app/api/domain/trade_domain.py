import uuid
from datetime import datetime
from sqlalchemy.orm import Session
from db.models import Trade, User, Market
from models.schema import TradeCreateModel, TradeResponseModel, ResponseModel
from models.response import Http

def trade_validations(trade: TradeCreateModel, user: User | None, market: Market | None):
    response, _ = validate_user_and_market(user, market)
    if response.status != Http.StatusOk:
        return response, None
    response, _ = validate_trade_option(trade, market)
    if response.status != Http.StatusOk:
        return response, None
    response, _ = validate_user_balance(user, trade)
    if response.status != Http.StatusOk:
        return response, None
    return ResponseModel(status=Http.StatusOk, message="Trade created successfully"), None

def validate_user_and_market(user: User | None, market: Market | None):
    if not user or not market:
        return ResponseModel(status=Http.StatusNotFound, message="User or Market not found"), None

def validate_trade_option(trade: TradeCreateModel, market: Market):
    if trade.option not in market.options:
        return ResponseModel(status=Http.StatusBadRequest, message="Invalid option for this market"), None

def validate_user_balance(user: User, trade: TradeCreateModel):
    if user.balance < trade.amount:
        return ResponseModel(status=Http.StatusBadRequest, message="Insufficient balance"), None


def create_trade_response(trade: TradeCreateModel, db: Session) -> tuple[ResponseModel, TradeResponseModel]:
    try:
        user = (
            db.query(User)
            .filter(User.id == trade.user_id)
            .first()
        )
        market = (
            db.query(Market)
            .filter(Market.id == trade.market_id)
            .first()
        )

        response, _ = trade_validations(trade, user, market)
        if response.status != Http.StatusOk:
            return response, None

        new_trade = Trade(
            id=str(uuid.uuid4()),
            user_id=trade.user_id,
            market_id=trade.market_id,
            option=trade.option,
            amount=trade.amount,
            price=trade.price,
            type=trade.type,
            status="COMPLETED",
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

        user.balance -= trade.amount

        db.add(new_trade)
        db.add(user)
        db.commit()
        db.refresh(new_trade, user)

        trade_response = TradeResponseModel(
            id=str(new_trade.id),
            user_id=str(new_trade.user_id),
            market_id=str(new_trade.market_id),
            option=new_trade.option,
            amount=new_trade.amount,
            price=new_trade.price,
            type=new_trade.type,
        )
        return ResponseModel(
            status=Http.StatusOk,
            message="Trade created successfully"
        ), trade_response
    except Exception as e:
        return ResponseModel(
            status=Http.StatusInternalServerError,
            message=str(e)
        ), None
