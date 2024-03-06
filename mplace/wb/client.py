from datetime import datetime, date
from typing import Optional

import requests
from requests import Response, Request

from mplace.utils import ClientBase
from .models import Order, Sale, RealizationRow, StatRow, Stock


class ClientError(Exception):
    pass


class NoData(ClientError):
    pass


class ToManyRequests(ClientError):
    pass


class Client(ClientBase):
    client_secret: str

    def __init__(self, client_secret: str):
        self.client_secret = client_secret
        self.session = requests.Session()

    def _check_errors(self, resp: Response):
        data = resp.json()

        if data is None:
            raise NoData('Response data is None')

        if 'code' in data and data['code'] == 429:
            raise ToManyRequests('Too many requests')

    def _auth(self, req: Request) -> Request:
        req.headers = {
            **req.headers,
            'Authorization': self.client_secret
        }

        return req

    def get_orders(self, date_from: datetime, flag: int = 0) -> [Order]:
        """
        Заказы

        Документация: https://openapi.wb.ru/statistics/api/ru/#tag/Statistika/paths/~1api~1v1~1supplier~1orders/get

        :param date_from: Дата и время последнего изменения по заказу.
        :param flag: Описание параметра в документации WB
        :return: Список объектов Order
        """

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

    def get_sales(self, date_from: datetime, flag: int = 0) -> [Sale]:
        """
        Продажи и возвраты

        Документация: https://openapi.wb.ru/statistics/api/ru/#tag/Statistika/paths/~1api~1v1~1supplier~1sales/get

        :param date_from: Дата и время последнего изменения по продаже/возврату
        :param flag: Описание параметра в документации WB
        :return: Список объектов Sale
        """

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

    def get_stocks(self, date_from: datetime) -> [Stock]:
        """
        Склад

        Документация: https://openapi.wb.ru/statistics/api/ru/#tag/Statistika/paths/~1api~1v1~1supplier~1stocks/get

        :param date_from: Дата и время последнего изменения по товару
        :return: Список объектов Stock
        """

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

    def get_realization_report(self, date_from: datetime, date_to: datetime, limit=100000, rrdid=None) -> [
        RealizationRow]:
        """
        Отчет о продажах по реализации

        Документация: https://openapi.wb.ru/statistics/api/ru/#tag/Statistika/paths/~1api~1v1~1supplier~1reportDetailByPeriod/get

        :param date_from: Начальная дата отчета
        :param date_to: Конечная дата отчета
        :param limit: Максимальное количество строк отчета, возвращаемых методом. Не может быть более 100000
        :param rrdid: Уникальный идентификатор строки отчета. Необходим для получения отчета частями

        :return: Список объектов RealizationRow
        """

        params = {
            'dateFrom': date_from.strftime('%Y-%m-%dT%H:%M:%S'),
            'dateTo': date_to.strftime('%Y-%m-%dT%H:%M:%S'),
            'limit': limit
        }

        if rrdid is not None:
            params['rrdid'] = rrdid

        data = self._get(
            'https://statistics-api.wildberries.ru/api/v1/supplier/reportDetailByPeriod',
            params=params
        )

        def _str_to_dt(value: Optional[str]) -> Optional[datetime]:
            return datetime.strptime(
                value.replace('Z', ''),
                '%Y-%m-%dT%H:%M:%S'
            ) if value is not None else None

        result = [RealizationRow(**{
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

        return result

    def get_stats_kt(self, date_from: date, date_to: date) -> [StatRow]:
        """
        Получение статистики КТ по дням

        Документация: https://openapi.wb.ru/analytics/api/ru/#tag/Voronka-prodazh/paths/~1content~1v1~1analytics~1nm-report~1grouped~1history/post

        :param date_from: Начало периода
        :param date_to: Конец периода
        :return: Список объектов StatRow
        """

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
