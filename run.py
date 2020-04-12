import os
import sys
from urllib.parse import urljoin, quote
from utils.GetCityUrls import GetCities
from spider.meituan import HttpRequest
from settings import KEYWORD
sys.path.append(os.path.abspath(__file__))


if __name__ == '__main__':
    urls = GetCities().get_city_urls()
    for url in urls:
        spider = HttpRequest(urljoin(url, 's/{}/'.format(quote(KEYWORD))), KEYWORD)
        spider.run()
