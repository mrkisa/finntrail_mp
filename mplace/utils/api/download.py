import os

import requests


def download_report(url, out_dir):
    """
    Скачивает отчет xlsx или csv

    :param url: Ссылка на отчет в формате xlsx или csv
    :param out_dir: Путь к папке, в которую будет скачан отчет
    :return: Путь к файлу с отчетом
    """
    report_file_name = url.split('/')[-1]
    report_file = os.path.join(out_dir, report_file_name)

    r = requests.get(url)
    with open(report_file, 'wb') as f:
        f.write(r.content)

    return report_file
