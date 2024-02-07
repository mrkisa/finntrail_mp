from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from mplace.utils import Base


class Stock(Base):
    __tablename__ = 'ozon_stocks'

    sku: Mapped[str] = mapped_column(String(100), primary_key=True)
    name: Mapped[str] = mapped_column(String(200))

    warehouse_id: Mapped[str] = mapped_column(String(20), primary_key=True)
    warehouse_name: Mapped[str] = mapped_column(String(50))

    items_available: Mapped[int]
    items_reserved: Mapped[int]
