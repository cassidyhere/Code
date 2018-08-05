from collections import OrderedDict
import hashlib

# consistent hashing
class ConsistentHash:
    def __init__(self, hashFunction, numberOfReplicas, nodes):
        '''初始化hash,添加节点

        self.circle存放节点映射关系,key为节点hash值,value为节点,根据key排序.排序为方便get

        Args:
            hashFunction: hash函数
            numberOfReplicas: 虚拟节点数量
            nodes: 节点,可迭代对象
        '''

        self.hashFunction = hashFunction
        self.numberOfReplicas = numberOfReplicas
        self.circle = OrderedDict()

        for node in nodes:
            self.add(node)

    def add(self, node):
        '''增加节点

        self.circle增加numberOfReplicas个节点，随后重新排序

        Args:
            node: 节点
        '''

        for i in range(self.numberOfReplicas):
            self.circle[self.hashFunction(node + str(i))] = node
        self.circle = OrderedDict(sorted(self.circle.items(), key=lambda x: x[0]))

    def remove(self, node):
        '''删除节点

        Args:
            node: 节点
        '''

        for i in range(self.numberOfReplicas):
            self.circle.pop(self.hashFunction(node + str(i)))

    def get(self, key):
        '''获取节点

        获取第一个hash值大于等于key的hash值的节点,若没有,返回self.circle第一个节点.若self.circle为空,返回None

        Args:
            key

        Return:
            node节点
        '''
        if not self.circle:
            return
        hash = self.hashFunction(key)
        for node in self.circle.keys():
            if hash <= node:
                return self.circle[node]
        return list(self.circle.values())[0]

def hashFunction(key):
    return hashlib.md5(key.encode('utf-8')).hexdigest()

if __name__ == '__main__':
    nodes = ['0.0.0.0', '0.0.0.1', '0.0.0.2']
    ch = ConsistentHash(hash, 3, nodes)
    print(ch.circle)
    ch.remove('0.0.0.1')
    print(ch.circle)
    ch.add('0.0.0.3')
    print(ch.circle)
    for i in ['dfas', 'fadsf', 'hy', 'hahgadg', '4zdfg6']:
        print(ch.get(i))

        