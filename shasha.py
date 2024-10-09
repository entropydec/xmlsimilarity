"""
zhangshasha 算法的 python 实现
"""
from nlpV1.descriptor_processes import XML
import class2char


class Tree:
    """
    输入为xml字符串，输出一颗树
    """

    def __init__(self, xml):
        """
        :param xml: 已经读入的xml字符串
        """
        self.l = []  # 将每个节点的 leftmost 节点的 index 按照后序遍历的顺序存放于 self.l 中
        self.keyroots = []  # 见函数 getKeyroots()
        self.labels = []  # 将每个节点的 label 按照后序遍历的顺序存放于 self.l
        xmlProcess = XML.XmlProcess()
        self.root = xmlProcess.getTree(xml)
        self.dlrList = []

    def traverse(self):
        """
        按照后序遍历的顺序给每个节点打上标签，这里使用节点的 class 类型的映射作为 label
        :return: 给每个节点添加 label 属性，并按照后序遍历的顺序存放于 self.labels 中
        """
        labelList = []
        self.labels = list(self._traverse(self.root, labelList))
        # print(''.join(self.labels))

    def _traverse(self, node, labelList):
        for child in node:
            labelList = self._traverse(child, labelList)
        labelList.append(class2char.class2char(node.get('class')))
        # labelList.append(node.get('class'))
        return labelList

    def index(self):
        """
        按照后根遍历方法给节点进行数字标记
        :return: 给每个节点添加 index 属性
        """
        self._index(self.root, 0)

    def _index(self, node, i):
        for child in node:
            i = self._index(child, i)
        i += 1
        node.set('index', i)
        return i

    def getL(self):
        """
        将每个节点的 leftmost 节点的 index 按照后序遍历的顺序存放于 self.l 中
        :return: 存放于 self.l中
        """
        self.leftmost()
        lList = []
        self.l = self._getL(self.root, lList)
        # print(self.l)

    def _getL(self, node, lList):
        for child in node:
            lList = self._getL(child, lList)
        lList.append(node.get('leftmost').get('index'))
        return lList

    def leftmost(self):
        """
        获取每个节点的 所有 子孙节点中 最靠左的一个节点
        :return: 给每个节点添加 leftmost 属性
        """
        self._leftmost(self.root)

    def _leftmost(self, node):
        if node is None:
            return None
        for child in node:
            self._leftmost(child)
        if len(node) == 0:
            node.set('leftmost', node)
        else:
            node.set('leftmost', node[0].get('leftmost'))

    def getKeyroots(self):
        """
        keyroots: 根节点 以及 只出现在'右子树'中的，只有一个子节点(即左子树)的节点或没有子节点的节点
                                这里的右子树指具有左兄弟节点的其他除了最左边兄弟节点的子节点
        keyroots(T) = {k | there exists no k’> k such that/(k)= l(k’)}.
        :return: 包含所有 keytoot 节点的集合 self.keyroots
        """
        for i in range(0, len(self.l)):
            flag = False
            for j in range(i + 1, len(self.l)):
                if self.l[i] == self.l[j]:
                    flag = True
                    break
            if flag is False:
                self.keyroots.append(i + 1)
        # print(self.keyroots)

    def post(self):
        """
        对树进行后序遍历
        :param root: xml树的根节点
        :return: 根据后序遍历得到的xml树的叶子节点的列表
        """
        self._post(self.root)
        dlrList = list(self.dlrList)
        self.dlrList = []
        return dlrList

    def _post(self, root):
        for child in root:
            self._post(child)
        self.dlrList.append(root.get('index'))

class ZhangShasha:
    def __init__(self):
        self.TD = []

    def shashaAlg(self, tree1: Tree, tree2: Tree):
        """
        Zhangshasha 算法
        :param tree1: 树1
        :param tree2: 树2
        :return: 两棵树的编辑距离
        """
        tree1.index()
        tree1.getL()
        tree1.getKeyroots()
        tree1.traverse()
        tree2.index()
        tree2.getL()
        tree2.getKeyroots()
        tree2.traverse()
        # print(tree1.post())
        # print(tree2.post())

        l1 = list(tree1.l)
        keyroots1 = list(tree1.keyroots)
        l2 = list(tree2.l)
        keyroots2 = list(tree2.keyroots)

        self.TD = [[0 for _ in range(len(l2) + 1)] for _ in range(len(l1) + 1)]

        for i1, root1 in enumerate(keyroots1, start=1):
            for j1, root2 in enumerate(keyroots2, start=1):
                i = root1
                j = root2
                self.TD[i][j] = self.treeDist(l1, l2, i, j, tree1, tree2)
        # print('\n')
        # for i in selfTD.:
        #     print(i)
        return self.TD[len(l1)][len(l2)]

    def treeDist(self, l1, l2, i, j, tree1, tree2):
        """
        计算 subtree(l1[i - 1], i + 1) 和 subtree(l2[j - 1], j + 1) 之间的距离
        :param l1: self.l
        :param l2: self.l
        :param i: root 的 index
        :param j: root 的 index
        :param tree1: xml树
        :param tree2: xml树
        :return: subtree(l1[i - 1], i + 1) 和 subtree(l2[j - 1], j + 1) 之间的距离
        """
        forestdist = [[0 for _ in range(j + 1)] for _ in range(i + 1)]

        Delete = 1
        Insert = 1
        Relabel = 1

        forestdist[0][0] = 0
        for i1 in range(l1[i - 1], i + 1):
            forestdist[i1][0] = forestdist[i1 - 1][0] + Delete
        for j1 in range(l2[j - 1], j + 1):
            forestdist[0][j1] = forestdist[0][j1 - 1] + Insert
        for i1 in range(l1[i - 1], i + 1):
            for j1 in range(l2[j - 1], j + 1):
                i_tmp = 0 if (l1[i - 1] > i1 - 1) else (i1 - 1)
                j_tmp = 0 if (l2[j - 1] > j1 - 1) else (j1 - 1)
                if l1[i1 - 1] == l1[i - 1] and l2[j1 - 1] == l2[j - 1]:
                    Cost = 0 if tree1.labels[i1 - 1] == tree2.labels[j1 - 1] else Relabel
                    forestdist[i1][j1] = min(min(forestdist[i_tmp][j1] + Delete, forestdist[i1][j_tmp] + Insert),
                                             forestdist[i_tmp][j_tmp] + Cost)
                    self.TD[i1][j1] = forestdist[i1][j1]
                else:
                    i1_tmp = l1[i1 - 1] - 1
                    j1_tmp = l2[j1 - 1] - 1
                    i_tmp2 = 0 if (l1[i - 1] > i1_tmp) else i1_tmp
                    j_tmp2 = 0 if (l2[j - 1] > j1_tmp) else j1_tmp
                    forestdist[i1][j1] = min(min(forestdist[i_tmp][j1] + Delete, forestdist[i1][j_tmp] + Insert),
                                             forestdist[i_tmp2][j_tmp2] + self.TD[i1][j1]);

        return forestdist[i][j]


if __name__ == '__main__':
    file1 = "/Users/apple/Desktop/23.xml"
    file_o1 = open(file1)
    xml1 = file_o1.read()
    file2 = "/Users/apple/Desktop/23.xml"
    file_o2 = open(file2)
    xml2 = file_o2.read()
    tree1 = Tree(xml1)
    tree2 = Tree(xml2)
    ss = ZhangShasha()
    print(ss.shashaAlg(tree1, tree2))
