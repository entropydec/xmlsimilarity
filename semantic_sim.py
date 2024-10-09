"""
基于语义和结构的xml相似度计算
用于对比实验
"""
"""
本方法聚合了三种比较方式：路径之间的映射，前序遍历子节点之间的映射，中序遍历子节点之间的映射
目前已经实现了第一种方法，但是只得到了最佳匹配序列的总和，不知道除以什么，目前的想法是除以min(len1,len2)
后面两种方法我觉得不好实现，因为我没法进行不同维度的比较，若是不考虑维度只进行比较，则两种方法得到的结果是一样的
有一种方法是用空格进行组合然后对句子进行wmdistance的比较，我认为效果较差
"""
from nlpV1.descriptor_processes import XML
from nlpV1.get_string import getString
from nlpV1.NLPProcess import NLPProcess
import class2char
import func


class SemanticSim:
    def __init__(self, nlpProecss):
        self.nlpProecss = nlpProecss
        self.dlrList = []
        self.lrdList = []

    def getTree(self, xml):
        """
        :param xml: 已经读入的xml字符串
        :return: xml树经过预处理的根节点
        """
        xmlProcess = XML.XmlProcess()
        root = xmlProcess.getTree(xml)
        return root

    def dlr(self, root):
        """
        对树进行前序遍历，其结果和后序遍历的结果相同
        :param root: xml树的根节点
        :return: 根据前序遍历得到的xml树的叶子节点的列表
        """
        self._dlr(root)
        dlrList = list(self.dlrList)
        self.dlrList = []
        return dlrList

    def _dlr(self, root):
        if len(root) == 0:
            self.dlrList.append(root)
        else:
            for child in root:
                self._dlr(child)

    def lrd(self, root):
        """
        对树进行后序遍历（对应二叉树的中序遍历）
        :param root: xml树的根节点
        :return: 根据前序遍历得到的xml树的叶子节点的列表
        """
        for child in root:
            self.lrd(child)
        if len(root) == 0:
            self.lrdList.append(root)

    def generatePath(self, root):
        """
        遍历 XML 树，获取从根节点起始的所有路径
        :param root: 根节点
        :return: 路径集合
        """
        paths = []
        stack_node = []
        self._generatePath(root, paths, stack_node)
        return paths

    def _generatePath(self, root, paths, stack_node):
        stack_node.append(root)
        if len(root) == 0:
            paths.append(stack_node.copy())
        else:
            for child in root:
                self._generatePath(child, paths, stack_node)
        stack_node.pop()

    def pathSim(self, path1, path2):
        """
        比较两条节点路径的相似度，由 非叶子节点路径的相似度 和 叶子节点之间的相似度 加权得出
        :param path1: 路径 1
        :param path2: 路径 2
        :return: 路径相似度
        """
        # 非叶子节点路径的相似度：使用字符串编辑距离计算
        string1 = class2char.path2string(path1)
        string2 = class2char.path2string(path2)
        dis = func.stringDistance(string1, string2)
        sim1 = 1 - (dis / max(len(string1), len(string2)))
        # print(sim1)

        # 叶子节点之间的相似度：使用nlp模型计算
        nodeString1 = getString.getNodeString(path1[-1])
        nodeString2 = getString.getNodeString(path2[-1])
        sim2 = self.nlpProecss.run(nodeString1, nodeString2, 'token')
        # print(sim2)

        # TODO: 目前权重为 6:4, 因为后面又使用了叶子结点，因此我认为非叶子节点的权重应该更高
        sim = 0.6 * sim1 + 0.4 * sim2
        return sim

    # 测试用
    def getLeaves(self, xml1, xml2):
        """
        计算存放于 self.lrdList 中的叶子节点的相似度
        :param xml1: xml字符串1
        :param xml2: xml字符串2
        :return: 叶子节点的相似度
        """
        root1 = self.getTree(xml1)
        nodeList1 = self.dlr(root1)
        root2 = self.getTree(xml2)
        nodeList2 = self.dlr(root2)

    def leafSim(self, xml1, xml2):
        """
        计算存放于 self.lrdList 中的叶子节点的相似度
        :param xml1: xml字符串1
        :param xml2: xml字符串2
        :return: 叶子节点的相似度
        """
        root1 = self.getTree(xml1)
        nodeList1 = self.dlr(root1)
        root2 = self.getTree(xml2)
        nodeList2 = self.dlr(root2)
        allNodeString1 = ''
        allNodeString2 = ''
        for node in nodeList1:
            allNodeString1 += getString.node2String(node)
        for node in nodeList2:
            allNodeString2 += getString.node2String(node)
        # print(allNodeString1)
        # print(allNodeString2)
        sim = self.nlpProecss.run(allNodeString1, allNodeString2, 'string')
        return sim

    def xmlSim(self, xml1, xml2):
        """
        传入的参数是两个xml的字符串
        :param xml1: xml字符串1
        :param xml2: xml字符串2
        :return: 两个xml之间的基于语义和结构之间的相似度, TODO:目前给出的是加权和，但是不知道该除什么，先除 min(len1, len2)
        """
        root1 = self.getTree(xml1)
        paths1 = self.generatePath(root1)
        root2 = self.getTree(xml2)
        paths2 = self.generatePath(root2)
        # for path in paths1:
        #     str123 = '/'
        #     for i in path:
        #         str123 += i.get('class') + '/'
        #     # print(str123)
        #     print(class2char.path2string(path))
        len1 = len(paths1)
        len2 = len(paths2)
        # km算法要求len2 >= len1，因此需要分两种情况
        if len2 >= len1:
            s = [[0 for col in range(len2)] for row in range(len1)]
            for i, p1 in enumerate(paths1):
                for j, p2 in enumerate(paths2):
                    s[i][j] = int(self.pathSim(p1, p2) * 1000)
            # for s1 in s:
            #     print(s1)
            Km = func.KM(s, len1, len2, None, None)
            ans = Km.km2() / min(len1, len2)
        else:
            s = [[0 for col in range(len1)] for row in range(len2)]
            for i, p1 in enumerate(paths2):
                for j, p2 in enumerate(paths1):
                    s[i][j] = int(self.pathSim(p1, p2) * 1000)
            Km = func.KM(s, len2, len1, None, None)
            ans = Km.km2() / min(len1, len2)
        return ans * 1.0 / 1000


if __name__ == '__main__':
    file1 = "/Users/apple/Desktop/2.xml"
    file_o1 = open(file1)
    xml1 = file_o1.read()
    file2 = "/Users/apple/Desktop/11.xml"
    file_o2 = open(file2)
    xml2 = file_o2.read()
    semanticSim = SemanticSim()
    # print(semanticSim.leafSim(xml1, xml2))
    print(semanticSim.xmlSim(xml1, xml2))
