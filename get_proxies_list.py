import requests
from odo import odo
from scrapy.http import TextResponse


def parse_row(row):
	els = row.css('td')
	ip = els[0].css('::text').extract_first()
	port = els[1].css('::text').extract_first()
	return "http://{}:{}".format(ip, port)


def get_list(url):
	r = requests.get(url)
	rows = response.css('tr')
	proxies = [[parse_row(row)] for row in rows[1:]]
	return proxies


def get_proxy_csv():
    url = "https://incloak.com/proxy-list/?maxtime=2000&type=h#list"
	proxies = get_list(url)
	odo(proxies, 'data/proxies.csv')


if __name__ == '__main__':
    get_proxy_csv()
