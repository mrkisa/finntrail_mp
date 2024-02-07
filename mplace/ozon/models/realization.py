from datetime import date

from sqlalchemy import String, Date, Integer
from sqlalchemy.orm import Mapped, mapped_column

from mplace.utils import Base


class Realization(Base):
    __tablename__ = 'ozon_realization'

    doc_date: Mapped[date] = mapped_column(Date, primary_key=True)
    row_number: Mapped[int] = mapped_column(Integer, primary_key=True)

    product_id: Mapped[str] = mapped_column(String(50))
    product_name: Mapped[str] = mapped_column(String(200))
    offer_id: Mapped[str] = mapped_column(String(200))
    barcode: Mapped[str] = mapped_column(String(200))
    price: Mapped[float]
    commission_percent: Mapped[float]
    price_sale: Mapped[float]
    sale_qty: Mapped[int]
    sale_amount: Mapped[float]
    sale_discount: Mapped[float]
    sale_commission: Mapped[float]
    sale_price_seller: Mapped[float]
    return_sale: Mapped[float]
    return_qty: Mapped[int]
    return_amount: Mapped[float]
    return_discount: Mapped[float]
    return_commission: Mapped[float]
    return_price_seller: Mapped[float]
