from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker

class Base(DeclarativeBase):
    pass

engine = create_engine("sqlite:///biblioteca.db")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) 