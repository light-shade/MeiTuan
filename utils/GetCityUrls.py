import requests
from lxml import etree
from urllib.parse import urljoin


class GetCities(object):
    def __init__(self):
        self.host = 'https://www.meituan.com/changecity/'

    def get_city_urls(self):
        resp = requests.get(
            self.host,
            headers={
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
            }
        ).content.decode('utf-8')
        doc = etree.HTML(resp)
        city_urls = doc.xpath('//div[@class="city-area"]/span[@class="cities"]/a/@href')
        city_urls = [urljoin(self.host, city_url) for city_url in city_urls]
        return city_urls
