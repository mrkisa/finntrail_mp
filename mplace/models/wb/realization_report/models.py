from datetime import datetime

from sqlalchemy import String, Float, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from mplace.models.base import Base


class WBReportRow(Base):
    """
    Отчет о продажах по реализации

    Платформа: Wildberries
    Ссылка на документацию апи: https://openapi.wb.ru/statistics/api/ru/#tag/Statistika/paths/~1api~1v1~1supplier~1reportDetailByPeriod/get
    """

    __tablename__ = "wb_realization_report"

    rrd_id: Mapped[int] = mapped_column(String(50), primary_key=True)

    realizationreport_id: Mapped[int]
    date_from: Mapped[datetime]
    date_to: Mapped[datetime]
    create_dt: Mapped[datetime]
    currency_name: Mapped[str] = mapped_column(String(20))
    suppliercontract_code: Mapped[str] = mapped_column(String(100), nullable=True, default=None)
    gi_id: Mapped[int]
    subject_name: Mapped[str] = mapped_column(String(200))
    nm_id: Mapped[int]
    brand_name: Mapped[str] = mapped_column(String(50))
    sa_name: Mapped[str] = mapped_column(String(200))
    ts_name: Mapped[str] = mapped_column(String(200))
    barcode: Mapped[str] = mapped_column(String(30))
    doc_type_name: Mapped[str] = mapped_column(String(30))
    quantity: Mapped[int]
    retail_price: Mapped[float]
    retail_amount: Mapped[float]
    sale_percent: Mapped[int]
    commission_percent: Mapped[float]
    office_name: Mapped[str] = mapped_column(String(200), nullable=True, default=None)
    supplier_oper_name: Mapped[str] = mapped_column(String(200), nullable=True, default=None)
    order_dt: Mapped[datetime] = mapped_column(DateTime, nullable=True, default=None)
    sale_dt: Mapped[datetime] = mapped_column(DateTime, nullable=True, default=None)
    rr_dt: Mapped[datetime] = mapped_column(DateTime, nullable=True, default=None)
    shk_id: Mapped[int] = mapped_column(String(50), primary_key=True)
    retail_price_withdisc_rub: Mapped[float] = mapped_column(Float, nullable=True, default=None)
    delivery_amount: Mapped[int] = mapped_column(Integer, nullable=True, default=None)
    return_amount: Mapped[int] = mapped_column(Integer, nullable=True, default=None)
    delivery_rub: Mapped[float] = mapped_column(Float, nullable=True, default=None)
    gi_box_type_name: Mapped[str] = mapped_column(String(200), nullable=True, default=None)
    product_discount_for_report: Mapped[float] = mapped_column(Float, nullable=True, default=None)
    supplier_promo: Mapped[float] = mapped_column(Float, nullable=True, default=None)
    rid: Mapped[int] = mapped_column(String(50), nullable=True, default=None)
    ppvz_spp_prc: Mapped[float] = mapped_column(Float, nullable=True, default=None)
    ppvz_kvw_prc_base: Mapped[float] = mapped_column(Float, nullable=True, default=None)
    ppvz_kvw_prc: Mapped[float] = mapped_column(Float, nullable=True, default=None)
    sup_rating_prc_up: Mapped[float] = mapped_column(Float, nullable=True, default=None)
    is_kgvp_v2: Mapped[float] = mapped_column(Float, nullable=True, default=None)
    ppvz_sales_commission: Mapped[float] = mapped_column(Float, nullable=True, default=None)
    ppvz_for_pay: Mapped[float] = mapped_column(Float, nullable=True, default=None)
    ppvz_reward: Mapped[float] = mapped_column(Float, nullable=True, default=None)
    acquiring_fee: Mapped[float] = mapped_column(Float, nullable=True, default=None)
    acquiring_bank: Mapped[str] = mapped_column(String(200), nullable=True, default=None)
    ppvz_vw: Mapped[float] = mapped_column(Float, nullable=True, default=None)
    ppvz_vw_nds: Mapped[float] = mapped_column(Float, nullable=True, default=None)
    ppvz_office_id: Mapped[int] = mapped_column(Integer, nullable=True, default=None)
    ppvz_office_name: Mapped[str] = mapped_column(String(200), nullable=True, default=None)
    ppvz_supplier_id: Mapped[int] = mapped_column(Integer, nullable=True, default=None)
    ppvz_supplier_name: Mapped[str] = mapped_column(String(200), nullable=True, default=None)
    ppvz_inn: Mapped[str] = mapped_column(String(50), nullable=True, default=None)
    declaration_number: Mapped[str] = mapped_column(String(50), nullable=True, default=None)
    bonus_type_name: Mapped[str] = mapped_column(String(200), nullable=True, default=None)
    sticker_id: Mapped[str] = mapped_column(String(200), nullable=True, default=None)
    site_country: Mapped[str] = mapped_column(String(50), nullable=True, default=None)
    penalty: Mapped[float] = mapped_column(Float, nullable=True, default=None)
    additional_payment: Mapped[float] = mapped_column(Float, nullable=True, default=None)
    rebill_logistic_cost: Mapped[float] = mapped_column(Float, nullable=True, default=None)
    rebill_logistic_org: Mapped[str] = mapped_column(String(200), nullable=True, default=None)
    kiz: Mapped[str] = mapped_column(String(50), nullable=True, default=None)
    srid: Mapped[str] = mapped_column(String(50), nullable=True, default=None)
