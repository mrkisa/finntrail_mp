from sqlalchemy.orm import Session

from mplace.wb import Client, RealizationRow


def sync(date_from, date_to, client: Client, session: Session):
    """Записывает Отчет о продажах по реализации за период date_from - date_to"""

    items: [RealizationRow] = client.get_realization_report(date_from, date_to)
    for item in items:
        session.merge(item)

    session.commit()
