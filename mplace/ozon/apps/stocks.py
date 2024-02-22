from sqlalchemy.orm import Session
from mplace.ozon import Client, Stock
from mplace.utils import download_report, read_excel


def sync(warehouses_ids, data_dir, client: Client, session: Session):
    """Записывает Отчёт об остатках на FBS-складе"""

    report_code = client.create_stock_report(warehouses_ids)
    report_url = client.get_report_info(report_code)
    report_file = download_report(report_url, data_dir)

    for row in read_excel(report_file, sheet_index=0):
        warehouse_id, warehouse_name, sku, name, available, reserved = row

        stock = Stock(
            sku=sku,
            name=name,
            warehouse_id=warehouse_id,
            warehouse_name=warehouse_name,
            items_available=available,
            items_reserved=reserved
        )

        session.merge(stock)

    session.commit()
