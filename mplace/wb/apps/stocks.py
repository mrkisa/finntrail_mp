from sqlalchemy.orm import Session

from mplace.wb import Client, Stock


def sync(date_from, client: Client, session: Session):
    """Записывает информацию об остатках на Складе за дату date_from"""

    items: [Stock] = client.get_stocks(date_from=date_from)
    for item in items:
        session.merge(item)

    session.commit()
