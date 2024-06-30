from sqlalchemy import String, ForeignKey, Integer, select, Table, Column
from sqlalchemy.orm import Mapped, relationship, mapped_column, selectinload

from database.base import Base, Manager

user_value_table = Table(
    "user_values", Base.metadata,
    Column("user_id", ForeignKey("user.id"), primary_key=True),
    Column("value_id", ForeignKey("value.id"), primary_key=True), )


class UserManager(Manager):

    async def add_values(self: 'User', values: list[str]) -> None:
        async with self.connection.session as session:
            # Getting current user with his values
            user = (await session.execute(
                select(User).options(selectinload(User.values)).filter(User.id == self.id))).scalar_one()

            # Determine values which doesn't exist
            user_value_names = {user_value.name.lower() for user_value in user.values}
            values_for_add = {value.lower() for value in values if value not in user_value_names}

            if values_for_add:
                # Getting all values from DB
                existing_values = (await session.execute(
                    select(Value).where(Value.name.in_(values_for_add)))).scalars().all()
                existing_value_names = {value.name.lower() for value in existing_values}

                for value in values_for_add:
                    if value in existing_value_names:
                        # The value exists into DB, that just create connection
                        existing_value = next(ev for ev in existing_values if ev.name == value)
                        user.values.append(existing_value)

                    else:
                        # The value isn't exists, create value and to make new connection
                        new_value = Value(name=value)
                        session.add(new_value)
                        user.values.append(new_value)

                await session.commit()


class User(Base, UserManager):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    telegram_id: Mapped[int] = mapped_column(Integer, unique=True)
    thread_id: Mapped[str] = mapped_column(String(255))
    values: Mapped[list["Value"]] = relationship(back_populates='users', secondary=user_value_table, lazy='selectin')

    def __str__(self):
        return f"User <id:{self.id}, id_tel:{self.telegram_id}, id_thread:{self.thread_id}>"

    def __repr__(self):
        return self.__str__()


class Value(Base):
    __tablename__ = "value"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), unique=True)
    users: Mapped[list["User"]] = relationship(back_populates='values', secondary=user_value_table, lazy='selectin')

    def __str__(self):
        return f"Value <id:{self.id}, name:{self.name}>"

    def __repr__(self):
        return self.__str__()
