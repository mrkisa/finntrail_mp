from datetime import datetime

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from mplace.models.base import Base


class WBSale(Base):
    """
    Продажи

    Платформа: Wildberries
    Ссылка на документацию апи: https://openapi.wb.ru/statistics/api/ru/#tag/Statistika/paths/~1api~1v1~1supplier~1sales/get
    """

    __tablename__ = "wb_sales"

    srid: Mapped[str] = mapped_column(String(255), primary_key=True)

    date: Mapped[datetime]
    lastChangeDate: Mapped[datetime]
    warehouseName: Mapped[str] = mapped_column(String(50))
    countryName: Mapped[str] = mapped_column(String(200))
    oblastOkrugName: Mapped[str] = mapped_column(String(200))
    regionName: Mapped[str] = mapped_column(String(200))
    supplierArticle: Mapped[str] = mapped_column(String(75))
    nmId: Mapped[int]
    barcode: Mapped[str] = mapped_column(String(30))
    category: Mapped[str] = mapped_column(String(50))
    subject: Mapped[str] = mapped_column(String(50))
    brand: Mapped[str] = mapped_column(String(50))
    techSize: Mapped[str] = mapped_column(String(30))
    incomeID: Mapped[int]
    isSupply: Mapped[bool]
    isRealization: Mapped[bool]
    totalPrice: Mapped[int]
    discountPercent: Mapped[int]
    spp: Mapped[int]
    forPay: Mapped[float]
    finishedPrice: Mapped[int]
    priceWithDisc: Mapped[int]
    saleID: Mapped[str] = mapped_column(String(15))
    orderType: Mapped[str] = mapped_column(String(100))
    sticker: Mapped[str] = mapped_column(String(100))
    gNumber: Mapped[str] = mapped_column(String(50))
