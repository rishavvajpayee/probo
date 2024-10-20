from pydantic import BaseModel
from datetime import datetime
from typing import List


class UserModel(BaseModel):
    username: str
    email: str
    password: str
    balance: float | None = None


class UserResponseModel(BaseModel):
    id: str
    username: str
    email: str
    balance: float


class MarketModel(BaseModel):
    question: str
    description: str
    close_date: datetime
    options: List[str]
    creator_id: str


class MarketResponseModel(BaseModel):
    id: str
    question: str
    description: str
    close_date: datetime
    options: List[dict]
    creator_id: str


class TradeModel(BaseModel):
    user_id: str
    market_id: str
    option: str
    amount: float
    price: float
    type: str


class TradeResponseModel(BaseModel):
    id: str
    user_id: str
    market_id: str
    option: str
    amount: float
    price: float
    type: str


class MarketCreateModel(BaseModel):
    question: str
    description: str
    close_date: datetime
    options: List[str]
    creator_id: str


class TradeCreateModel(BaseModel):
    user_id: str
    market_id: str
    option: str
    amount: float
    price: float
    type: str


class ResponseModel(BaseModel):
    status: int
    message: str


class FastAPIResponseWrapper(BaseModel):
    response: ResponseModel
    data: (
        UserResponseModel
        | List[UserResponseModel]
        | MarketResponseModel
        | List[MarketResponseModel]
        | TradeResponseModel
        | List[TradeResponseModel]
        | None
    )
