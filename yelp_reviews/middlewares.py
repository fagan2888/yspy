import os
import random
from scrapy.conf import settings
from stem import Signal
from stem.control import Controller


class ProxyMiddleware(object):

    def process_request(self, request, spider):
        request.meta['proxy'] = random.choice(settings.get('PROXY_LIST'))
