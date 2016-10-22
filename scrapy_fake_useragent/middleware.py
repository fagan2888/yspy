from fake_useragent import UserAgent


class RandomUserAgentMiddleware(object):

    def __init__(self):
        super(RandomUserAgentMiddleware, self).__init__()
        self.useragent = UserAgent()

    def process_request(self, request, spider):
        request.headers.setdefault('User-Agent', self.useragent.random)
