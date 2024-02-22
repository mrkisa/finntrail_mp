from sqlalchemy.orm import Session

from mplace.wb import Client, StatRow


def sync(date_from, date_to, client: Client, session: Session):
    """Записывает Статистику по КТ за период date_from - date_to"""

    items: [StatRow] = client.get_stats_kt(date_from=date_from, date_to=date_to)
    for item in items:
        session.merge(item)

    session.commit()
