'''
TODO表与Visited表

TODO表: 存放未爬取的url
Visited表: 存放已爬取的url
'''

from collections import deque
from array import array

class TODO:
    '''TODO列表

    存放未爬取的url.实现get/put/isEmpty方法,方便使用其他数据结构替换
    此处get方法为先进先出,单线程下相当于宽度优先的爬虫
    '''
    def __init__(self):
        self.deque = deque()

    def get(self):
        return self.deque.popleft()

    def put(self, x):
        self.deque.append(x)

    def isEmpty(self):
        return len(self.deque) == 0

class Visited:
    '''Visited列表

    存放已爬取的url,要求快速查找元素和添加元素.使用hash值节省空间.
    实现in/add方法,方便使用其他数据结构替换
    '''
    def __init__(self):
        self.visited = set()

    def __contains__(self, item):
        if hash(item) in self.visited:
            return True
        else:
            return False

    def add(self, item):
        self.visited.add(hash(item))

    def remove(self, item):
        h = hash(item)
        if h in self:
            self.visited.remove(h)

class BloomFilter:
    '''一个简单的布隆过虑器,Visited表的一种方案

    当Visited表数据量太大,为了节省空间与查找时间,使用布隆过虑器,缺点是存可能发生误判
    '''
    def __init__(self, size, hash_count, hash_fun):
        '''
        Args:
            size: 布隆过虑器的容器大小.例如需要存放1亿个url,映射8个哈希值,则size可以选择16亿,size大小回影响误判率
            hash_count: hash次数,hash_count大小回影响误判率
            hash_fun: hash函数,hash_fun应能均匀映射到size大小的空间
        '''
        self.size = size
        self.visited = array('b', [0] * size)
        self.hash_count = hash_count
        self.hash_fun = hash_fun

    def __contains__(self, item):
        '''判断item是否在self.visited中

        若self.visited中item的某个hash值对应位置为0,则item不在self.visited中
        '''
        for i in range(self.hash_count):
            if self.visited[self.hash_fun(item + str(i))] == 0:
                return False
        return True

    def add(self, item):
        '''添加item到self.visited中

        将self.visited中item的hash_count个hash值对应位置设为1
        '''
        for i in range(self.hash_count):
            self.visited[self.hash_fun(item + str(i))] = 1
