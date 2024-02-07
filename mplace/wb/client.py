from datetime import datetime, date
from typing import Optional

import requests
from requests import Response, Request

from mplace.utils import ClientBase
from .models import Order, Sale, RealizationRow, StatRow, Stock


class Client(ClientBase):
    client_secret: str

    def __init__(self, client_secret: str):
        self.client_secret = client_secret
        self.session = requests.Session()

    def _check_errors(self, resp: Response):
        data = resp.json()
        if 'code' in data and data['code'] == 429:
            raise Exception('Too many requests')

    def _auth(self, req: Request) -> Request:
        req.headers = {
            **req.headers,
            'Authorization': self.client_secret
        }

        return req

    def get_orders(self, date_from: datetime, flag: int = 0) -> [Order]:
        data = self._get(
            'https://statistics-api.wildberries.ru/api/v1/supplier/orders',
            params={
                'dateFrom': date_from.strftime('%Y-%m-%dT%H:%M:%S'),
                'flag': flag
            }
        )

        return [Order(**{
            **row,
            'date': datetime.strptime(row['date'], '%Y-%m-%dT%H:%M:%S'),
            'lastChangeDate': datetime.strptime(row['lastChangeDate'], '%Y-%m-%dT%H:%M:%S'),
            'cancelDate': datetime.strptime(row['cancelDate'], '%Y-%m-%dT%H:%M:%S'),
        }) for row in data]

    def get_sales(self, date_from: datetime, flag: int = 0):
        data = self._get(
            'https://statistics-api.wildberries.ru/api/v1/supplier/sales',
            params={
                'dateFrom': date_from.strftime('%Y-%m-%dT%H:%M:%S'),
                'flag': flag
            }
        )

        return [Sale(**{
            **row,
            'date': datetime.strptime(row['date'], '%Y-%m-%dT%H:%M:%S'),
            'lastChangeDate': datetime.strptime(row['lastChangeDate'], '%Y-%m-%dT%H:%M:%S'),
        }) for row in data]

    def get_stocks(self, date_from: datetime):
        data = self._get(
            'https://statistics-api.wildberries.ru/api/v1/supplier/stocks',
            params={
                'dateFrom': date_from.strftime('%Y-%m-%dT%H:%M:%S')
            }
        )

        return [Stock(**{
            **row,
            'lastChangeDate': datetime.strptime(row['lastChangeDate'], '%Y-%m-%dT%H:%M:%S'),
        }) for row in data]

    def get_realization_report(self, date_from: datetime, date_to: datetime):
        data = self._get(
            'https://statistics-api.wildberries.ru/api/v1/supplier/reportDetailByPeriod',
            params={
                'dateFrom': date_from.strftime('%Y-%m-%dT%H:%M:%S'),
                'dateTo': date_to.strftime('%Y-%m-%dT%H:%M:%S')
            }
        )

        def _str_to_dt(value: Optional[str]) -> Optional[datetime]:
            return datetime.strptime(
                value.replace('Z', ''),
                '%Y-%m-%dT%H:%M:%S'
            ) if value is not None else None

        return [RealizationRow(**{
            **row,
            'date_from': _str_to_dt(row['date_from']),
            'date_to': _str_to_dt(row['date_to']),
            'create_dt': _str_to_dt(row['create_dt']),
            'order_dt': _str_to_dt(row['order_dt']),
            'sale_dt': _str_to_dt(row['sale_dt']),
            'rr_dt': _str_to_dt(row['rr_dt']),

            'rid': str(row['rid']),
            'rrd_id': str(row['rrd_id']),
            'shk_id': str(row['shk_id'])
        }) for row in data]

    def get_stats_kt(self, date_from: date, date_to: date):
        data = self._post(
            'https://suppliers-api.wildberries.ru/content/v1/analytics/nm-report/grouped/history',
            json={
                'period': {
                    'begin': date_from.strftime('%Y-%m-%d'),
                    'end': date_to.strftime('%Y-%m-%d')
                }
            }
        )

        return [StatRow(**{
            **row,
            'dt': datetime.strptime(row['dt'], '%Y-%m-%d').date()
        }) for row in data['data'][0]['history']]
