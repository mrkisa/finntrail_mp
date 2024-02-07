from datetime import datetime
from typing import List

from sqlalchemy import String, ForeignKey, Table, Column, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from mplace.utils import Base


class Item(Base):
    __tablename__ = 'ozon_items'

    sku: Mapped[str] = mapped_column(String(50), primary_key=True)
    name: Mapped[str] = mapped_column(String(200))


transactions_items = Table(
    'ozon_transaction_items',
    Base.metadata,
    Column('transaction_id', ForeignKey('ozon_transactions.operation_id')),
    Column('item_id', ForeignKey('ozon_items.sku')),
)


class Service(Base):
    __tablename__ = 'ozon_transaction_services'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    transaction_id: Mapped[str] = mapped_column(ForeignKey('ozon_transactions.operation_id'))
    transaction: Mapped['Transaction'] = relationship(back_populates='services')

    name: Mapped[str] = mapped_column(String(200))
    price: Mapped[float]


class Transaction(Base):
    __tablename__ = 'ozon_transactions'

    operation_id: Mapped[str] = mapped_column(String(50), primary_key=True)

    operation_type: Mapped[str] = mapped_column(String(200))
    operation_date: Mapped[datetime]
    operation_type_name: Mapped[str] = mapped_column(String(200))
    delivery_charge: Mapped[int]
    return_delivery_charge: Mapped[int]
    accruals_for_sale: Mapped[int]
    sale_commission: Mapped[int]
    amount: Mapped[float]
    type: Mapped[str] = mapped_column(String(25))

    posting_delivery_schema: Mapped[str] = mapped_column(String(50), nullable=True)
    posting_order_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    posting_number: Mapped[str] = mapped_column(String(50), nullable=True)
    posting_warehouse_id: Mapped[str] = mapped_column(String(50))

    items: Mapped[List[Item]] = relationship(secondary=transactions_items)
    services: Mapped[List[Service]] = relationship()
