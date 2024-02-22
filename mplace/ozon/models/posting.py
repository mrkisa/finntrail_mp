from datetime import datetime

from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from mplace.utils import Base


class Posting(Base):
    __tablename__ = 'ozon_postings'

    order_number: Mapped[str] = mapped_column(String(20))  # Номер заказа
    posting_number: Mapped[str] = mapped_column(String(20), primary_key=True)  # Номер отправления
    delivery_schema: Mapped[str] = mapped_column(String(3))  # Схема работы — FBO или FBS
    in_process_at: Mapped[datetime]  # Принят в обработку
    shipment_date: Mapped[datetime] = mapped_column(DateTime, nullable=True, default=None)  # Дата отгрузки
    status: Mapped[str] = mapped_column(String(20))  # Статус
    delivery_date: Mapped[datetime] = mapped_column(DateTime, nullable=True, default=None)  # Дата доставки
    posting_sum: Mapped[float]  # Сумма отправления
    posting_currency_code: Mapped[str] = mapped_column(String(3))  # Код валюты отправления
    product_name: Mapped[str] = mapped_column(String(200))  # Наименование товара
    sku: Mapped[str] = mapped_column(String(20))  # OZON id
    offer_id: Mapped[str] = mapped_column(String(100))  # Артикул
    product_amount: Mapped[float]  # Итоговая стоимость товара
    product_currency_code: Mapped[str] = mapped_column(String(3))  # Код валюты товара
    qty: Mapped[int]  # Количество
    delivery_price: Mapped[float]  # Стоимость доставки
    buyback: Mapped[str] = mapped_column(String(200))  # Выкуп товара
    price: Mapped[float]  # Цена товара до скидок
    total_discount_percent: Mapped[float]  # Скидка %
    total_discount_value: Mapped[float]  # Скидка руб
    promo: Mapped[str] = mapped_column(String(200))  # Акции
