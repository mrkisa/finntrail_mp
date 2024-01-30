from datetime import datetime

from sqlalchemy import String, Integer, SmallInteger
from sqlalchemy.orm import Mapped, mapped_column

from mplace.models.base import Base


class WBStock(Base):
    """
    Склад

    Платформа: Wildberries
    Ссылка на документацию апи: https://openapi.wb.ru/statistics/api/ru/#tag/Statistika/paths/~1api~1v1~1supplier~1stocks/get
    """

    __tablename__ = "wb_stocks"

    nmId: Mapped[int] = mapped_column(Integer, primary_key=True)

    lastChangeDate: Mapped[datetime]
    warehouseName: Mapped[str] = mapped_column(String(50))
    supplierArticle: Mapped[str] = mapped_column(String(75))
    barcode: Mapped[str] = mapped_column(String(30))
    quantity: Mapped[int]
    inWayToClient: Mapped[int] = mapped_column(SmallInteger)
    inWayFromClient: Mapped[int] = mapped_column(SmallInteger)
    quantityFull: Mapped[int]
    category: Mapped[str] = mapped_column(String(50))
    subject: Mapped[str] = mapped_column(String(50))
    brand: Mapped[str] = mapped_column(String(50))
    techSize: Mapped[str] = mapped_column(String(30))
    Price: Mapped[float]
    Discount: Mapped[float]
    isSupply: Mapped[bool]
    isRealization: Mapped[bool]
    SCCode: Mapped[str] = mapped_column(String(50))
