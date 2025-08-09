from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
import os

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Series(Base):
    __tablename__ = "series"
    id = Column(Integer, primary_key=True)
    source = Column(String, index=True)
    remote_id = Column(String, index=True)
    title = Column(String)
    cover = Column(String, nullable=True)
