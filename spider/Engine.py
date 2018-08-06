'''
Engine与其子类负责具体的页面抓取.

Engine的子类需要实现run方法,其工作流程为:
1.当满足条件时,从TODO表取出一个url
2.抓取url对应页面内容,抓取成功则将返回的response对象交给Spider的parse_response方法处理
3.将该url添加到Visited表
'''

import requests
import threading
from spider.Vector import TODO, Visited

class Engine:
    '''Engine完成一些初始化工作

    初始化工作包括TODO表与Visited表,将Spider类中的urls添加至TODO表
    '''
    unvisited = TODO()
    visited = Visited()

    def __init__(self, spider, *args, **kwargs):
        self.spider = spider(*args, **kwargs)

        for url in self.spider.urls:
            if url not in self.visited:
                self.unvisited.put(url)

    def run(self):
        'crawl from unvisited'
        pass

# 简单的单线程版本
class SimpleEngine(Engine):
    def run(self):
        while self.unvisited.isEmpty() is False:
            url = self.unvisited.get()
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    try:
                        self.spider.parse_response(response)
                    except:
                        # Spider异常处理
                        pass
                else:
                    # 状态码的处理
                    pass
            except:
                # requests异常处理
                pass
            finally:
                # 添加至visited表
                self.visited.add(url)

# 多线程版本
RLock = threading.RLock()
class ThreadEngine(Engine):
    def run(self):
        while True:
            RLock.acquire()
            url = None if self.unvisited.isEmpty() else self.unvisited.get()
            RLock.release()
            if not url:
                break
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    try:
                        RLock.acquire()
                        self.spider.parse_response(response)
                        RLock.release()
                    except:
                        # Spider异常处理
                        pass
                else:
                    # 状态码的处理
                    pass
            except:
                # requests异常处理
                pass
            finally:
                # 添加至visited表
                RLock.acquire()
                self.visited.add(url)
                RLock.release()

    def thread_run(self, thread_num):
        threads = []
        for _ in range(thread_num):
            threads.append(threading.Thread(target=self.run, args=()))

        for thread in threads:
            thread.start()
            
# 协程版本
class CoroutineEngine(Engine):
    def run(self):
        pass
