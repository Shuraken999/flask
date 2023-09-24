import atexit
import os
import sqlalchemy as sq

from sqlalchemy import Column, DateTime, Integer, String, create_engine, func
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

PG_USER = os.getenv("PG_USER", "postgres")
PG_PASSWORD = os.getenv("PG_PASSWORD", "123456")
PG_DB = os.getenv("PG_DB", "app")
PG_HOST = os.getenv("PG_HOST", "127.0.0.1")
PG_PORT = os.getenv("PG_PORT", 5432)


PG_DSN = f"postgresql://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DB}"
engine = create_engine(PG_DSN)
atexit.register(engine.dispose)

Session = sessionmaker(bind=engine)
Base = declarative_base(bind=engine)


# class User(Base):
#     __tablename__ = "app_users"
#
#     id = Column(Integer, primary_key=True)
#     email = Column(String, nullable=False, unique=True, index=True)
#     password = Column(String, nullable=False)
#     owner = Column(String, nullable=False)
#     creation_time = Column(DateTime, server_default=func.now())


class Ads(Base):
    __tablename__ = "ads"

    id = Column(Integer, primary_key=True)
    user = Column(Integer, nullable=False, unique=True, index=True)
    heading = Column(String, nullable=False, unique=True, index=True)
    description = Column(String)
    # user_id = Column(Integer, sq.ForeignKey("user.id"), nullable=False)
    creation_time = Column(DateTime, server_default=func.now())

    # user = relationship(User, backref="ads")


Base.metadata.create_all()

