from sqlalchemy import Integer, String, Text, ForeignKey
#from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, async_scoped_session, create_async_engine
from sqlalchemy.orm import declarative_base, declared_attr, Mapped, mapped_column

#from tehpst_project.constants import ASYNC_CONNECTION_STRING


class PreBase:
    @declared_attr
    def __tablename__(self):
        return self.__name__.lower()
    id: Mapped[int] = mapped_column(Integer, primary_key=True)

Base = declarative_base(cls=PreBase)

class ProductUrl(Base):
    url: Mapped[str] = mapped_column(Text, nullable=False)
    product_name: Mapped[str] = mapped_column(String(512), nullable=False)


class FullProduct(Base):
    name: Mapped[str] = mapped_column(String(512), nullable=True)
    art: Mapped[str] = mapped_column(String(128), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    slug: Mapped[str] = mapped_column(String(128), nullable=False, default='')
#    country :Mapped[str] = mapped_column(String(50), default='')
    quantity: Mapped[str] = mapped_column(String(10))
    price: Mapped[str] = mapped_column(String(10))
    brand_name: Mapped[str] = mapped_column(String(50), nullable=True)


class Stocks(Base):
    stock_name: Mapped[str] = mapped_column(String(128), nullable=False)
    stock_quantity: Mapped[str] = mapped_column(String(10))
    product_id: Mapped[int] = mapped_column(ForeignKey('fullproduct.id', ondelete='CASCADE'))


class Product_property(Base):
    property_name: Mapped[str] = mapped_column(String(128), nullable=False)
    property_value: Mapped[str] = mapped_column(String(128), nullable=True)
    product_id: Mapped[int] = mapped_column(ForeignKey('fullproduct.id', ondelete='CASCADE'))
