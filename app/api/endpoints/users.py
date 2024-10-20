
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.database import get_db
from models.schema import UserModel, UserResponseModel, FastAPIResponseWrapper
from api.domain.user_domain import create_user_response, get_users_response

users = []

USER_ROUTES = APIRouter()

@USER_ROUTES.post("/users", response_model=FastAPIResponseWrapper)
def create_user(user: UserModel, db: Session = Depends(get_db)):
    response, data = create_user_response(user, db)
    return FastAPIResponseWrapper(response=response, data=data)


@USER_ROUTES.get("/all-users", response_model=FastAPIResponseWrapper)
def get_users(db: Session = Depends(get_db)):
    response, data = get_users_response(db)
    return FastAPIResponseWrapper(response=response, data=data)

@USER_ROUTES.get("/users/{user_id}", response_model=FastAPIResponseWrapper)
def get_user(user_id: str, db: Session = Depends(get_db)):
    response, data = get_users_response(db, user_id)
    return FastAPIResponseWrapper(response=response, data=data)
