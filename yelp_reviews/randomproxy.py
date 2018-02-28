# Daniil Mashkin <daniil.mashkin@gmail.com> (2016)
# based on https://github.com/aivarsk/scrapy-proxies

import re
import random
import base64
import logging
from scrapy.downloadermiddlewares.retry import RetryMiddleware

logger = logging.getLogger(__name__)


class RandomProxyRetryMiddleware(RetryMiddleware):
    def __init__(self, settings):
        RetryMiddleware.__init__(self, settings)
        self.proxy_list = settings.get('PROXY_LIST')

        self.proxies = {}
        for line in self.proxy_list:
            parts = re.match('(\w+://)(\w+:\w+@)?(.+)', line)

            # Cut trailing @
            if parts.group(2):
                user_pass = parts.group(2)[:-1]
            else:
                user_pass = ''

            self.proxies[parts.group(1) + parts.group(3)] = user_pass

    def process_request(self, request, spider):
        # Don't overwrite with a random one (server-side state for IP)
        if 'proxy' in request.meta:
            return

        self.change_proxy(request)

    def change_proxy(self, request):
        proxy_address = random.choice(self.proxies.keys())
        proxy_user_pass = self.proxies[proxy_address]

        request.meta['proxy'] = proxy_address
        if proxy_user_pass:
            basic_auth = 'Basic ' + base64.encodestring(proxy_user_pass)
            request.headers['Proxy-Authorization'] = basic_auth

    def _retry(self, request, reason, spider):
        retries = request.meta.get('retry_times', 0) + 1
        proxy = request.meta['proxy']
        logger.debug('Retrying proxy <%s> #%d: %s' % (proxy, retries, reason))
        retryreq = request.copy()
        retryreq.meta['retry_times'] = retries
        retryreq.dont_filter = True
        retryreq.priority = request.priority + self.priority_adjust

        if retries > self.max_retry_times:
            try:
                del self.proxies[proxy]
                self.change_proxy(retryreq)
                retryreq.meta['retry_times'] = 0
                logger.error('Removing proxy <%s>, %d proxies left' % (proxy, len(self.proxies)))
            except (ValueError, KeyError):
                pass

        return retryreq
