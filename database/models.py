from typing import List

from sqlalchemy import String, Table, ForeignKey, Column, select, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base, Manager
from database.connector import db_conn

user_values_table = Table(
    "user_values_table",
    Base.metadata,
    Column("user_left_id", ForeignKey("users.id"), primary_key=True),
    Column("value_right_id", ForeignKey("values.id"), primary_key=True), )


class User(Base, Manager):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    telegram_id: Mapped[int] = mapped_column(Integer, unique=True)
    thread_id: Mapped[str] = mapped_column(String(255))
    values: Mapped[List['Value']] = relationship(secondary=user_values_table, back_populates="users",
                                                 lazy="selectin")

    def __str__(self):
        return f"User <id:{self.id}, id_tel:{self.telegram_id}, id_thread:{self.thread_id}>"

    def __repr__(self):
        return self.__str__()

    async def add_values(self, values: List[str]) -> None:
        async with db_conn.session as session:
            model_values = [Value(description=item) for item in values]
            query = select(User).where(User.id == self.id)
            result = await session.execute(query)
            user = result.scalar()
            if user:
                session.add_all(model_values)

                user.values.extend(model_values)
                await session.commit()


class Value(Base, Manager):
    __tablename__ = "values"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    description: Mapped[str] = mapped_column(String(255), unique=True)
    users: Mapped[List['User']] = relationship(secondary=user_values_table, back_populates="values",
                                               lazy="selectin")

    def __str__(self):
        return f"Value <id:{self.id}, value:{self.value}>"

    def __repr__(self):
        return self.__str__()
