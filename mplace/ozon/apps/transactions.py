from sqlalchemy.orm import Session

from mplace.ozon import Client, Transaction


def sync(date_from, date_to, client: Client, session: Session):
    """Записывает Список транзакций за период date_from - date_to"""

    items: [Transaction] = client.get_transactions(date_from=date_from, date_to=date_to)
    for item in items:
        session.merge(item)

    session.commit()
