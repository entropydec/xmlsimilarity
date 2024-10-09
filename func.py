import Levenshtein


def stringDistance(string1, string2):
    """
    计算字符串编辑距离
    :param string1: 字符串1
    :param string2: 字符串2
    :return: 两个字符串直接的编辑距离
    """
    return Levenshtein.distance(string1, string2)


class KM:
    """
    KM算法：计算二分图的最佳匹配
    :要求! : n <= m
    :param w: 二分图的邻接矩阵
        这里要求每一个权值为 [0, 1000]之间的正整数，即计算出[0,1]之间的相似度后 * 1000 得到的 int 型整数
    :param n: 二分图左边节点的数量
    :param m: 二分图右边节点的数量
    """
    def __init__(self, w, n, m, list1, list2):
        self.w = w  # w数组记录边权值
        self.list1 = list1  # 存储节点的数组，用于生成匹配对
        self.list2 = list2
        self.line = [-1 for i in range(max(n, m))]  # line数组记录右边端点所连的左端点
        self.usex = [0 for i in range(n)]  # usex，usey数组记录是否曾访问过，也是判断是否在增广路上
        self.usey = [0 for i in range(m)]
        self.cx = [0 for i in range(n)]  # cx，cy数组就是记录点的顶标
        self.cy = [0 for i in range(m)]
        self.n = n  # n左
        self.m = m  # m右
        self.qwq = 99999  # 一个不可能达到的的较大值
        for i in range(0, n):
            d = 0
            for j in range(0, m):
                d = max(d, self.w[i][j])
            self.cx[i] = d
        # self.preprocess()

    def preprocess(self):
        """
        对 self.w 进行预处理，因为要进行匹配偏离度的计算，即在进行匹配的时候要确保不能匹配到距离自己太远的点
        :return: None
        """
        k = 50  # 这里设定偏差权值值为 50
        for i in range(0, self.n):
            for j in range(0, self.m):
                self.w[i][j] -= abs(i - j) * k
                self.w[i][j] = 0 if self.w[i][j] < 0 else self.w[i][j]
        print('\n')
        for i in self.w:
            print(i)

    def find(self, x):
        self.usex[x] = 1
        for i in range(0, self.m):
            if self.usey[i] == 0 and self.cx[x] + self.cy[i] == self.w[x][i]:  # 如果这个点未访问过并且它是子图里面的边
                self.usey[i] = 1
                if self.line[i] == -1 or self.find(self.line[i]):  # 如果这个点未匹配或者匹配点能更改
                    self.line[i] = x
                    return True
        return False

    def km(self):
        for i in range(0, self.n):
            while True:
                d = self.qwq
                self.usex = [0 for i in range(self.n)]
                self.usey = [0 for i in range(self.m)]
                if self.find(i):
                    break
                for j in range(0, self.n):
                    if self.usex[j]:
                        for k in range(0, self.m):
                            if not self.usey[k]:
                                d = min(d, self.cx[j] + self.cy[k] - self.w[j][k])
                if d == self.qwq:
                    return -1
                for j in range(0, self.n):
                    if self.usex[j]:
                        self.cx[j] -= d
                for j in range(0, self.m):
                    if self.usey[j]:
                        self.cy[j] += d
        ans = 0
        boundsList = {}
        classList = {}
        for i in range(0, self.m):
            if self.line[i] != -1:
                # print(self.w[self.line[i]][i])
                if self.list1[self.line[i]].get('leaf') is True and self.list2[i].get('leaf') is True:
                    if self.w[self.line[i]][i] >= 400:
                        boundsList[self.list1[self.line[i]].get('bounds')] = self.list2[i].get('bounds')
                        classList[str(self.list1[self.line[i]].get('class')) + str(self.list1[self.line[i]].get('bounds'))]\
                            = str(self.list2[i].get('class')) + str(self.list2[i].get('bounds'))
                ans += self.w[self.line[i]][i]
        # print(self.line)
        return ans, boundsList, classList

    def km2(self):
        """
        为比较方法写的km函数
        :return: km相似度
        """
        for i in range(0, self.n):
            while True:
                d = self.qwq
                self.usex = [0 for i in range(self.n)]
                self.usey = [0 for i in range(self.m)]
                if self.find(i):
                    break
                for j in range(0, self.n):
                    if self.usex[j]:
                        for k in range(0, self.m):
                            if not self.usey[k]:
                                d = min(d, self.cx[j] + self.cy[k] - self.w[j][k])
                if d == self.qwq:
                    return -1
                for j in range(0, self.n):
                    if self.usex[j]:
                        self.cx[j] -= d
                for j in range(0, self.m):
                    if self.usey[j]:
                        self.cy[j] += d
        ans = 0
        for i in range(0, self.m):
            if self.line[i] != -1:
                ans += self.w[self.line[i]][i]
        return ans


if __name__ == '__main__':
    string1 = 'hssdSrssrssrssHrrkrUkrUkrUrSrrrrrZ'
    string2 = 'hsSrkksHrhrssrqrsTsTrTrArrSZ'
    print(stringDistance(string1, string2))
    w = [[2, 6, 0, 0], [7, 0, 5, 0], [0, 6, 0, 5]]
    n = 3
    m = 4
    km = KM(w, n, m)
    s = [0.0] * m
    s = [s] * n
    print(km.km())
    print(s)
