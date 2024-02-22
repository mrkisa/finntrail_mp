from sqlalchemy.orm import Session

from mplace.wb import Client, Order


def sync_changed(date_from, client: Client, session: Session):
    """Записывает Заказы с обновлением после date_from"""

    items: [Order] = client.get_orders(date_from=date_from, flag=0)
    for item in items:
        session.merge(item)

    session.commit()


def sync_created(date_from, client: Client, session: Session):
    """Записывает Заказы с датой создания равной date_from, время date_from не учитывается"""

    items: [Order] = client.get_orders(date_from=date_from, flag=1)
    for item in items:
        session.merge(item)

    session.commit()
