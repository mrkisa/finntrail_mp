from datetime import datetime

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from mplace.utils import Base


class Order(Base):
    __tablename__ = 'wb_orders'

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
    finishedPrice: Mapped[int]
    priceWithDisc: Mapped[int]
    isCancel: Mapped[bool]
    cancelDate: Mapped[datetime]
    orderType: Mapped[str] = mapped_column(String(100))
    sticker: Mapped[str] = mapped_column(String(100))
    gNumber: Mapped[str] = mapped_column(String(50))
