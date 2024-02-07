import datetime

from sqlalchemy import Date
from sqlalchemy.orm import Mapped, mapped_column

from mplace.utils import Base


class StatRow(Base):
    __tablename__ = 'wb_stats_kt'

    dt: Mapped[datetime.date] = mapped_column(Date, primary_key=True)

    openCardCount: Mapped[int]
    addToCartCount: Mapped[int]
    addToCartConversion: Mapped[int]
    ordersCount: Mapped[int]
    ordersSumRub: Mapped[int]
    cartToOrderConversion: Mapped[int]
    buyoutsCount: Mapped[int]
    buyoutsSumRub: Mapped[int]
    buyoutPercent: Mapped[int]
