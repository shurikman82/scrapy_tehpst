from sqlalchemy import Integer, String, Text
#from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, async_scoped_session, create_async_engine
from sqlalchemy.orm import declarative_base, declared_attr, Mapped, mapped_column

#from tehpst_project.constants import ASYNC_CONNECTION_STRING


class PreBase:
    @declared_attr
    def __tablename__(self):
        return self.__name__.lower()
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

Base = declarative_base(cls=PreBase)

class ProductUrl(Base):
    product_name: Mapped[str] = mapped_column(String(512), nullable=False)
    url: Mapped[str] = mapped_column(Text, nullable=False)
