import bcrypt
from db.models import User
from models.schema import UserModel, UserResponseModel, ResponseModel
from models.response import Http
from sqlalchemy.orm import Session

def create_user_response(user: UserModel, db: Session) -> tuple[ResponseModel, UserResponseModel]:
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        return ResponseModel(status=Http.StatusBadRequest, message="User already exists"), None

    password_hash = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    new_user = User(
        username=user.username,
        email=user.email,
        password_hash=password_hash,
        balance=user.balance or 1000.00,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    user_response = UserResponseModel(
        id=str(new_user.id),
        username=new_user.username,
        email=new_user.email,
        balance=new_user.balance,
    )
    return ResponseModel(status=Http.StatusOk, message="User created successfully"), user_response


def get_users_response(db: Session, user_id: str | None = None) -> tuple[ResponseModel, UserResponseModel | list[UserResponseModel]]:
    user = None
    users = []
    if user_id:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return ResponseModel(status=Http.StatusNotFound, message="User not found"), None
    else:
        users = db.query(User).all()
    if user:
        return ResponseModel(status=Http.StatusOk, message="User fetched successfully"), UserResponseModel(
            id=str(user.id),
            username=user.username,
            email=user.email,
            balance=user.balance,
        )
    if users:
        return ResponseModel(status=Http.StatusOk, message="Users fetched successfully"), [UserResponseModel(
            id=str(user.id),
            username=user.username,
            email=user.email,
            balance=user.balance,
        ) for user in users]
    return ResponseModel(status=Http.StatusNotFound, message="No users found"), None

