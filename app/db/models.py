import uuid

from sqlalchemy import Column, ForeignKey, String, Text, Numeric, DateTime, func, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    balance = Column(Numeric(10, 2), nullable=False, default=1000.00)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class Market(Base):
    __tablename__ = 'markets'

    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    question = Column(Text, nullable=False)
    description = Column(Text)
    close_date = Column(DateTime(timezone=True), nullable=False)
    creator_id = Column(UUID, ForeignKey('users.id'), nullable=False)
    options = Column(JSON, nullable=False)
    status = Column(String(20), nullable=False, default='ACTIVE')
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class Trade(Base):
    __tablename__ = 'trades'

    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID, ForeignKey('users.id'), nullable=False)
    market_id = Column(UUID, ForeignKey('markets.id'), nullable=False)
    option = Column(String(255), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    type = Column(String(10), nullable=False)
    status = Column(String(20), nullable=False, default='COMPLETED')
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
