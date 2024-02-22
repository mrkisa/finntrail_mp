import datetime

from mplace.ozon import Posting
from mplace.utils import download_report, read_csv


def sync(processed_at_from, delivery_schema, data_dir, client, session, processed_at_to=None):
    """Записывает Отчёт об отправлениях"""

    report_code = client.create_postings_report(
        processed_at_from=processed_at_from,
        processed_at_to=processed_at_to,
        delivery_schema=delivery_schema
    )

    report_url = client.get_report_info(report_code)
    report_file = download_report(report_url, data_dir)

    for row in read_csv(report_file):
        posting = Posting(
            order_number=row[0],
            posting_number=row[1],
            delivery_schema=delivery_schema,
            in_process_at=datetime.datetime.strptime(row[2], '%Y-%m-%d %H:%M:%S'),
            shipment_date=datetime.datetime.strptime(row[3], '%Y-%m-%d %H:%M:%S'),
            status=row[4],
            delivery_date=datetime.datetime.strptime(row[5], '%Y-%m-%d %H:%M:%S') if row[5] else None,
            posting_sum=float(row[6]),
            posting_currency_code=row[7],
            product_name=row[8],
            sku=row[9],
            offer_id=row[10],
            product_amount=float(row[11]),
            product_currency_code=row[12],
            qty=int(row[13]),
            delivery_price=float(row[14]) if row[14] else 0.0,
            # related=row[15],
            buyback=row[16],
            price=float(row[17]),
            total_discount_percent=float(row[18].replace('%', '')),
            total_discount_value=float(row[19]),
            promo=row[20],
        )

        session.merge(posting)

    session.commit()
