'''
Spider及其子类定制初始urls,制定爬取页面成功后的处理规则.
爬取一个新的网站只需定制新的Spider子类并实现parse_response方法
'''

import math

class Spider:
    def __init__(self, urls):
        self.urls = list(urls)

    def parse_response(self, response):
        '''页面抓取成功后的处理函数

        Args:
            response: 页面抓取成功后的返回对象
        '''
        pass

class WeiboSpider(Spider):
    def parse_response(self, response):
        # 处理response,提取有关数据
        data = response.json()
        for item in data['data']['cards'][-1]:
            user = item['user']
            v = V()
            v.name = user['screen_name']
            v.follow_count = int(user['follow_count'])
            v.follower_count = int(user['follower_count'])
            v.desc = item['desc1']
            v.lfid = user['profile_url'].split('lfid=')[-1]
            self.handle(v)

    def handle(self, item):
        # 处理提取后的数据
        profile_url = 'https://m.weibo.cn/api/container/getIndex?containerid={}&page='.format(item.lfid)
        if profile_url + '1' not in self.visited:
            # 若url尚未爬取,添加至self.unvisited
            page_count = int(math.ceil(item.follow_count / 20.))
            for i in range(1, page_count+1):
                self.unvisited.put(profile_url + str(i))

            # 接下来处理item,存放数据库等操作

class V:
    def __init__(self):
        '''微博用户信息

        Args:
            name: 用户名称
            desc: 描述
            follow_count: 关注人数
            follower_count: 粉丝人数
            lfid: 关注用户url
        '''
        self.name = None
        self.desc = None
        self.follow_count = 0
        self.follower_count = 0
        self.lfid = None

    def __repr__(self):
        return '{}: {} 粉丝: {}'.format(self.name, self.desc, self.follower_count)

