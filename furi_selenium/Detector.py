import time
import os
import requests
from bs4 import BeautifulSoup


class Detector():
    item_list_ui_path = 'div.module_list_product_default.extend_four.extend_thumbnail_tall > ul > li'

    def __init__(self, driver, args):
        self.target_url = args.target_url
        self._count = 0
        self.driver = driver

    def get_valid_item_with_url(self):
        try:
            item_dict = {}
            item_list = BeautifulSoup(self._parsing_target_page(), 'html.parser').select(Detector.item_list_ui_path)

            for item in item_list:
                item_dict[item.contents[1]['href']] = 0 if '일시품절' in item.contents[7].text else 1

            return item_dict
        except Exception as e:
            print(e)

    def _parsing_target_page(self):
        try:
            self._count += 1
            if self._count % 300 == 0:
                self.driver.get('https://www.naver.com/')
            time.sleep(2)
            headers = {
                        'Accept':          os.environ['Accept'],
                        'Accept-Encoding': os.environ['AcceptEncoding'],
                        'Accept-Language': os.environ['AcceptLanguage'],
                        'Cache-Control':   os.environ['CacheControl'],
                        'Sec-fetch-dest':  os.environ['Secfetchdest'],
                        'Sec-fetch-mode':  os.environ['Secfetchmode'],
                        'User-Agent':      os.environ['UserAgent']}
            resp = self._get(headers)
            return resp.text
        except Exception as e:
            print(e)

    def _get(self, headers):
        try:
            return requests.get(self.target_url, headers=headers, timeout=3)
        except Exception:
            print('Exception and Retry')
            return self._get(headers)

