from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from datetime import datetime
import hashlib

DATABASE_URL = "sqlite:///./ledgerpulse.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    workspaces = relationship("Workspace", back_populates="owner")

class Workspace(Base):
    __tablename__ = "workspaces"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    type = Column(String, default="FREELANCE")  # FREELANCE, ENTERPRISE, PERSONAL
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    balance = Column(Float, default=25000.0)

    owner = relationship("User", back_populates="workspaces")
    transactions = relationship("TransactionRecord", back_populates="workspace")

class TransactionRecord(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    workspace_id = Column(Integer, ForeignKey("workspaces.id"), nullable=True)
    order_id = Column(String, unique=True, index=True)
    recipient = Column(String, nullable=False)
    category = Column(String, nullable=False)
    description = Column(String, nullable=False)
    currency = Column(String, default="USD")
    subtotal = Column(Float, default=0.0)
    tax = Column(Float, default=0.0)
    amount = Column(Float, nullable=False)
    status = Column(String, default="PAID")
    created_at = Column(DateTime, default=datetime.utcnow)

    workspace = relationship("Workspace", back_populates="transactions")

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
