import re

from sqlalchemy.orm import Session

from mplace.ozon import Client, Realization

DATE_PATTERN = re.compile(r'^\d\d\d\d-\d\d+$')


def sync(date: str, client: Client, session: Session):
    """Записывает Отчет о реализации за указанный месяц"""

    assert DATE_PATTERN.match(date), 'Отчетный период должен быть в формате %Y-%m'

    items: [Realization] = client.get_realization_report(report_date=date)
    for item in items:
        session.merge(item)

    session.commit()
