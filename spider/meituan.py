import re
import requests
import time
from urllib.parse import urljoin
from settings import HEADERS
from db.mysqlconn import MysqlConn


class HttpRequest(object):
    def __init__(self, city_url, keyword):
        self.city_url = city_url
        self.keyword = keyword
        self.headers = HEADERS
        self.session = requests.Session()
        self.__home_page_verify()
        self.break_sig = False

    def __home_page_verify(self):
        self.session.get('https://xa.meituan.com/', headers=self.headers)

    def __get_params(self):
        resp = self.session.get(self.city_url, headers=self.headers).content.decode('utf-8')
        # 获取城市id
        city_id = re.search('var environment = {cityid: (\d+)};', resp, re.S).group(1)
        # 获取uuid
        home_uuid = re.search('"uuid":"(.*?)"', resp).group(1)
        # 获取商铺总数
        total_count = re.search('"data":{"totalCount":(\d+),', resp, re.S).group(1)
        city_name = re.search('"name":"(.*?)",', resp).group(1)
        limit = re.search('"limit":(\d+),', resp, re.S).group(1)
        return city_id, home_uuid, total_count, limit, city_name

    def parse_page(self, per_num, city_id, home_uuid, limit, city_name):
        url = f'https://apimobile.meituan.com/group/v4/poi/pcsearch/{city_id}?'
        self.headers.update({
            'Referer': self.city_url,
        })
        params = {
            'uuid': home_uuid,
            'userid': '-1',
            'limit': limit,
            'offset': str(32 * per_num),
            'cateId': '-1',
            'q': self.keyword,
        }

        try:
            resp = self.session.get(url, headers=self.headers, params=params)
            print('请求开始')
            if resp.status_code == 200:
                items = resp.json().get('data', None).get('searchResult')
                if not items:
                    self.break_sig = True
                for item in items:
                    data = {
                        'id': item.get('id'),
                        'city_name': city_name,
                        'address': item.get('address'),
                        'title': item.get('title'),
                        'backCateName': item.get('backCateName'),
                        'areaname': item.get('areaname'),
                        'avgprice': item.get('avgprice'),
                        'avgscore': item.get('avgscore'),
                        'comments': item.get('comments'),
                        'phone': item.get('phone'),
                        'imageUrl': item.get('imageUrl'),
                    }
                    print(data)
                    yield data
            else:
                time.sleep(180)
                self.parse_page(per_num, city_id, home_uuid, limit, city_name)
        except Exception as e:
            time.sleep(180)
            print('获取失败, 睡一会儿')
            print(e.args)
            self.parse_page(per_num, city_id, home_uuid, limit, city_name)

    def run(self):
        city_id, home_uuid, total_count, limit, city_name = self.__get_params()
        num = 1
        mysql = MysqlConn()
        mysql.add_table()
        while True:
            if self.break_sig:
                break
            print('开始')
            data_list = self.parse_page(num, city_id, home_uuid, limit, city_name)
            for data in data_list:
                print(data)
                mysql.insert(data)
            print(num)
            num += 1
            time.sleep(1)


if __name__ == '__main__':
    spider = HttpRequest(urljoin(url, 's/%E5%B0%8F%E5%90%83/'), '餐饮')
    spider.run()

