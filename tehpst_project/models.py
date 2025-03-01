from sqlalchemy import Integer, String, Text, ForeignKey
from sqlalchemy.orm import declarative_base, declared_attr, Mapped, mapped_column


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
    art: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    slug: Mapped[str] = mapped_column(String(255), nullable=False, default='')
    quantity: Mapped[int]
    price: Mapped[float]
    brand_name: Mapped[str] = mapped_column(String(50), nullable=True)


class Stocks(Base):
    stock_name: Mapped[str] = mapped_column(String(128), nullable=False)
    stock_quantity: Mapped[int]
    product_id: Mapped[int] = mapped_column(ForeignKey('fullproduct.id', ondelete='CASCADE'))


class Product_property(Base):
    property_name: Mapped[str] = mapped_column(String(254), nullable=False)
    property_value: Mapped[str] = mapped_column(String(254), nullable=True)
    product_id: Mapped[int] = mapped_column(ForeignKey('fullproduct.id', ondelete='CASCADE'))
