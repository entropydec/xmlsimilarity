"""
基于树编辑距离的相似度计算
"""
import os
from shasha import ZhangShasha, Tree


class DistanceSim:
    def __init__(self):
        self.postList = []
        self.preList = []

    def pre(self, root):
        """
        对树进行前序遍历
        :param root: xml树的根节点
        :return: 根据前序遍历得到的xml树节点
        """
        self._pre(root)
        preList = list(self.preList)
        self.preList = []
        return preList

    def _pre(self, root):
        self.preList.append(root)
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
        return postList

    def _post(self, root):
        for child in root:
            self._post(child)
        self.postList.append(root)

    def xmlSim(self, xml1, xml2):
        """
        传入的参数是两个xml的字符串
        :param xml1: xml字符串1
        :param xml2: xml字符串2
        :return: 两个xml之间的基于树编辑距离之间的相似度
        """
        tree1 = Tree(xml1)
        tree2 = Tree(xml2)
        ss = ZhangShasha()
        dis = ss.shashaAlg(tree1, tree2)
        len1 = len(tree1.labels)
        len2 = len(tree2.labels)
        # print(dis, len1, len2)
        try:
            sim = 1 - dis / (len1 + len2)
        except ZeroDivisionError:
            sim = 1.0
        return sim


if __name__ == '__main__':
    file1 = "/Users/apple/Desktop/23.xml"
    file_o1 = open(file1)
    xml1 = file_o1.read()
    file2 = "/Users/apple/Desktop/22.xml"
    file_o2 = open(file2)
    xml2 = file_o2.read()
    ss = DistanceSim()
    print(ss.xmlSim(xml1, xml2))
