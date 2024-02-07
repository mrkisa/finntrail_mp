import logging
import time
from datetime import datetime

import requests
from requests import Request, Response

from mplace.utils import ClientBase
from .models import Transaction, Item, Service, Realization


class ReportError(Exception):
    pass


class Client(ClientBase):
    def __init__(self, client_id: str, client_secret: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.session = requests.Session()

    def _check_errors(self, resp: Response):
        assert resp.status_code == 200, 'Bad status code: {}'.format(resp.status_code)

    def _auth(self, req: Request) -> Request:
        req.headers = {
            **req.headers,
            'Client-Id': self.client_id,
            'Api-Key': self.client_secret,
        }

        return req

    def get_transactions(self, date_from: datetime, date_to: datetime, page: int = 1,
                         page_size: int = 1000) -> [Transaction]:
        """
        Список транзакций

        :param date_from: Начало периода
        :param date_to: Конец периода
        :param page: Номер страницы, возвращаемой в запросе
        :param page_size: Количество элементов на странице
        :return: Список объектов Transaction
        """

        data = self._post(
            'https://api-seller.ozon.ru/v3/finance/transaction/list',
            json={
                'filter': {
                    'date': {
                        'from': date_from.strftime('%Y-%m-%dT%H:%M:%S.000Z'),
                        'to': date_to.strftime('%Y-%m-%dT%H:%M:%S.000Z'),
                    }
                },
                'page': page,
                'page_size': page_size
            }
        )

        result = []
        for row in data['result']['operations']:
            items = [Item(**{
                **item_row,
                'sku': str(item_row['sku'])
            }) for item_row in row['items']]

            services = [Service(
                **service_row
            ) for service_row in row['services']]

            posting = row.pop('posting')

            row = {
                **row,
                'operation_id': str(row['operation_id']),
                'operation_date': datetime.strptime(row['operation_date'], '%Y-%m-%d %H:%M:%S'),
                'items': items,
                'services': services,
                'posting_delivery_schema': posting['delivery_schema'] if bool(posting['delivery_schema']) else None,
                'posting_order_date': datetime.strptime(
                    posting['order_date'],
                    '%Y-%m-%d %H:%M:%S'
                ) if bool(posting['order_date']) else None,
                'posting_number': posting['posting_number'] if bool(posting['posting_number']) else None,
                'posting_warehouse_id': str(posting['warehouse_id']),
            }

            result.append(Transaction(**row))

        return result

    def get_realization_report(self, report_date: str) -> [Realization]:
        """
        Отчёт о реализации товаров

        :param report_date: Отчётный период в формате YYYY-MM
        :return: Список объектов Realization
        """
        data = self._post(
            'https://api-seller.ozon.ru/v1/finance/realization',
            json={
                'date': report_date
            }
        )

        doc_date = datetime.strptime(data['result']['header']['doc_date'], '%Y-%m-%d').date()
        return [Realization(**{
            **row,
            'doc_date': doc_date,
            'product_id': str(row['product_id'])
        }) for row in data['result']['rows']]

    def create_stock_report(self, warehouse_id: [str]) -> str:
        """
        Отчёт об остатках на FBS-складе

        :param warehouse_id: Идентификаторы складов
        :return: Уникальный идентификатор отчёта
        """
        data = self._post(
            'https://api-seller.ozon.ru/v1/report/warehouse/stock',
            json={
                'warehouseId': warehouse_id
            }
        )

        return data['result']['code']

    def create_postings_report(self, processed_at_from, delivery_schema) -> str:
        """
        Отчёт об отправлениях

        :param processed_at_from: Время, когда заказ попал в обработку
        :param delivery_schema: Схема работы — FBO или FBS
        :return: Уникальный идентификатор отчёта
        """
        assert delivery_schema.lower() in ('fbo', 'fbs')

        data = self._post(
            'https://api-seller.ozon.ru/v1/report/postings/create',
            json={
                'filter': {
                    'processed_at_from': processed_at_from.strftime('%Y-%m-%dT%H:%M:%S.000Z'),
                    'delivery_schema': [
                        delivery_schema
                    ]
                }
            }
        )

        return data['result']['code']

    def get_report_info(self, code: str, attempts: int = 10, timeout: int = 20):
        """
        Информация об отчёте

        После создания отчета сервису нужно время на подготовку. Поэтому функция проверяет
        статус в ответе сервиса. Если отчет еще в процессе подготовки, ждет время timeout и
        повторно запрашивает отчет. Количество попыток ограничено.

        :param code: Уникальный идентификатор отчёта
        :param attempts: Количество попыток
        :param timeout: Время ожидания между попытками в секундах
        :return: Ссылка на XLSX-файл.
        """

        # подготовка файла может занять время, поэтому проверяем статус
        # и, если файл пока не готов, делаем новую попытку после паузы
        for i in range(attempts):
            data = self._post(
                'https://api-seller.ozon.ru/v1/report/info',
                json={
                    'code': code
                }
            )

            result = data['result']
            if result['status'] in ('waiting', 'processing'):
                logging.info('Current report status: %s', result['status'])
                time.sleep(timeout)
                continue

            if result['status'] != 'success':
                raise ReportError('Bad report status: %s', result['status'])

            return result['file']
        else:
            raise ReportError('Attempts exceeded')
