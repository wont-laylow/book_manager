from sqlalchemy import Column, Integer, String, ForeignKey

from .db import Base, engine

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key= True, index=True, autoincrement=True)
    title = Column(String, index=True)
    author = Column(String, index=True)
    description = Column(String)

Base.metadata.create_all(engine)
    