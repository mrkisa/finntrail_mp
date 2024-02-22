from sqlalchemy.orm import Session

from mplace.wb import Client, RealizationRow


def sync(date_from, date_to, client: Client, session: Session):
    """Записывает Отчет о продажах по реализации за период date_from - date_to"""

    rrdid = None
    while True:
        items: [RealizationRow] = client.get_realization_report(date_from, date_to, rrdid=rrdid)
        for item in items:
            session.merge(item)

        session.commit()

        if len(items) <= 100000:
            break

        rrdid = items[-1].rrd_id
