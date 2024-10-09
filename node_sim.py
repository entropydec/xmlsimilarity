"""
基于节点相似度的相似度计算
"""
import os
from nlpV1.descriptor_processes import XML
from nlpV1.get_string import getString
from nlpV1.NLPProcess import NLPProcess
import class2char
import func
from datebase import DateBase


class NodeSim:
    def __init__(self, nlpProecss):
        self.nlpProecss = nlpProecss
        self.postList = []
        self.preList = []
        self.index = 0
        self.db = DateBase()

    @staticmethod
    def getTree(xml):
        """
        :param xml: 已经读入的xml字符串
        :return: xml树经过预处理的根节点
        """
        xmlProcess = XML.XmlProcess()
        root = xmlProcess.getTree(xml)
        return root

    def pre(self, root):
        """
        对树进行前序遍历
        同时把节点的字符串进行一下预处理！！！
        :param root: xml树的根节点
        :return: 根据前序遍历得到的xml树节点
        """
        self._pre(root)
        preList = list(self.preList)
        self.preList = []
        self.index = 0
        return preList

    def _pre(self, root):
        self.preList.append(root)
        root.set('string', getString.getNodeString(root))
        root.set('preIndex', self.index)
        self.index += 1
        if len(root) == 0:  # 叶子节点
            root.set('leaf', True)
        else:
            root.set('leaf', False)
        for child in root:
            self._pre(child)

    def post(self, root):
        """
        对树进行后序遍历
        :param root: xml树的根节点
        :return: 根据后序遍历得到的xml树节点
        """
        self._post(root)
        postList = list(self.postList)
        self.postList = []
        self.index = 0
        return postList

    def _post(self, root):
        for child in root:
            self._post(child)
        self.postList.append(root)
        root.set('postIndex', self.index)
        self.index += 1

    @staticmethod
    def preprocess(node1, node2, sim):
        """
        对 sim 进行预处理，因为要进行匹配偏离度的计算，即在进行匹配的时候要确保不能匹配到距离自己太远的点
        :return: 减去距离偏差之后的 前序相似度和后序相似度 的均值
        """
        k = 50  # 这里设定偏差权值值为 50
        preSim = sim - abs(node1.get('preIndex') - node2.get('preIndex')) * k
        preSim = 0 if preSim < 0 else preSim
        postSim = sim - abs(node1.get('postIndex') - node2.get('postIndex')) * k
        postSim = 0 if postSim < 0 else postSim
        return int((preSim + postSim) / 2)

    def _listSim(self, len1, len2, list1, list2):
        """
        因为要求 len1 < len2，因此单独写一个函数方便分类
        """
        s = [[0 for _ in range(len2)] for _ in range(len1)]
        for i, p1 in enumerate(list1):
            for j, p2 in enumerate(list2):
                classSim = 1 if class2char.class2char(p1.get('class')) == class2char.class2char(
                    p2.get('class')) else 0
                stringSim = self.nlpProecss.run(p1.get('string'), p2.get('string'), 'token')
                if p1.get('leaf') is True and p2.get('leaf') is True:  # 叶子节点之间的比较
                    sim = 0.3 * classSim + 0.7 * stringSim
                elif p1.get('leaf') is False and p2.get('leaf') is False:  # 非叶子结点之间的比较
                    sim = 0.7 * classSim + 0.3 * stringSim
                else:
                    sim = 0
                s[i][j] = NodeSim.preprocess(p1, p2, int(sim * 1000))
        # for s1 in s:
        #     print(s1)
        Km = func.KM(s, len1, len2, list1, list2)
        ans, boundsList, classList = Km.km()
        return (ans / min(len1, len2)), boundsList, classList

    def listSim(self, list1, list2):
        """
        计算两个节点数组的相似度
        :param list1: 节点数组1
        :param list2: 节点数组2
        :return:
        """
        len1 = len(list1)
        len2 = len(list2)
        if len2 >= len1:
            return self._listSim(len1, len2, list1, list2)
        else:
            # 需要更改一下 boundsList 的顺序
            ans, boundsList, classList = self._listSim(len2, len1, list2, list1)
            bound_new = {value: key for key, value in boundsList.items()}
            class_new = {value: key for key, value in classList.items()}
            return ans, bound_new, class_new

    def nodeSim(self, xml1, xml2):
        """
        计算存放于 self.lrdList 中的叶子节点的相似度
        :param xml1: xml字符串1
        :param xml2: xml字符串2
        :return: 叶子节点的相似度
        """
        root1 = NodeSim.getTree(xml1)
        preList1 = self.pre(root1)
        postList1 = self.post(root1)
        root2 = NodeSim.getTree(xml2)
        preList2 = self.pre(root2)
        postList2 = self.post(root2)
        preSim, boundsList, classList = self.listSim(preList1, preList2)
        # print(boundsList)
        # print('\n')
        self.db.storeMatchedList(matchedList=boundsList)
        self.db.readDb()
        return (preSim / 1000), classList


if __name__ == '__main__':
    file1 = "/Users/apple/Desktop/data/Shopping/1/more options.xml"
    file_o1 = open(file1)
    xml1 = file_o1.read()
    file2 = "/Users/apple/Desktop/data/Shopping/4/update shop.xml"
    file_o2 = open(file2)
    xml2 = file_o2.read()
    nlp = NLPProcess()
    ss = NodeSim(nlp)
    sim, classList = ss.nodeSim(xml1, xml2)
    print(sim)
