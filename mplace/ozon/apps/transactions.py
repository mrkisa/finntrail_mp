from sqlalchemy.orm import Session

from mplace.ozon import Client, Transaction


def sync(date_from, date_to, client: Client, session: Session):
    """Записывает Список транзакций за период date_from - date_to"""

    page = 1
    while True:
        transactions: [Transaction] = client.get_transactions(date_from=date_from, date_to=date_to, page=page)
        for transaction in transactions:
            known_transaction: [Transaction] = session.query(Transaction).get(transaction.operation_id)

            if known_transaction is not None:
                continue

            transaction.items = [session.merge(item) for item in transaction.items]

            session.add(transaction)

        session.commit()

        if len(transactions) < 1000:
            break

        page += 1
