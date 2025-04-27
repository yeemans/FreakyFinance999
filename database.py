from typing import List
from typing import Optional
from sqlalchemy import String, Float, Integer
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import create_engine, Column, String, Float, Integer, ForeignKey, Date
from sqlalchemy.orm import relationship


engine = create_engine("sqlite:///database.db", echo=True)
connection = engine.connect()

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    UserID: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(40), unique=True)
    password_hash: Mapped[str] = mapped_column(String(40))
    sheets = relationship("Sheet", back_populates="user")

    def __repr__(self) -> str:
        return f"User({self.username})"
    
class Sheet(Base):
    __tablename__ = "sheets"
    SheetID: Mapped[int] = mapped_column(primary_key=True)
    UserID = Column(Integer, ForeignKey('users.UserID'))

    # json string storing all the expenses
    json_string: Mapped[str] = mapped_column(String(2000))
    user = relationship("User", back_populates="sheets")

    def __repr__(self) -> str:
        return f"User({self.username})"
Base.metadata.create_all(engine)