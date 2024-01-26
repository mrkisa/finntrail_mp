import datetime

from sqlalchemy import Date
from sqlalchemy.orm import Mapped, mapped_column

from mplace.models.base import Base


class WBStatRow(Base):
    """
    Статистика КТ

    Платформа: Wildberries
    Ссылка на документацию апи: https://openapi.wb.ru/analytics/api/ru/#tag/Voronka-prodazh/paths/~1content~1v1~1analytics~1nm-report~1grouped~1history/post
    """

    __tablename__ = "wb_stats_kt"

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
