from spider.Item import V
from spider.TODO import TODO, Visited

class Spider:
    unvisited = TODO()
    visited = Visited()

    def parse_response(self, response):
        pass

    def run(self):
        for url in self.urls:
            if url not in self.visited:
                self.unvisited.put(url)

        'spider from unvisited. args: unvisited, visited'


class WeiboSpider(Spider):
    def __init__(self, urls):
        self.urls = list(urls)

    def parse_response(self, response):
        data = response.json()
        for item in data['data']['cards'][-1]:
            user = item['user']
            v = V()
            v.name = user['screen_name']
            v.follow_count = user['follow_count']
            v.follower_count = user['follower_count']
            v.desc = item['desc1']
            v.profile_url = 'https://m.weibo.cn/api/container/getIndex?containerid=' + user['profile_url'].split('lfid=')
            self.handle(v)

    def handle(self, item):
        if item.profile_url not in self.visited:
            self.unvisited.put(item.profile_url)
            '''save data
            '''

