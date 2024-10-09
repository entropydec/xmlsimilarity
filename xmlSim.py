"""
调用接口，计算相似度并画出对应的图片
"""
from distance_sim import DistanceSim
from node_sim import NodeSim
from image import ImageUtil
import os
import base64
from nlpV1.NLPProcess import NLPProcess


def xmlSim():
    # 计算相似度
    file1 = os.path.join(os.getcwd(), 'front_end', 'storage', 'a.xml')
    file_o1 = open(file1)
    xml1 = file_o1.read()
    file2 = os.path.join(os.getcwd(), 'front_end', 'storage', 'c.xml')
    file_o2 = open(file2)
    xml2 = file_o2.read()
    dissim = DistanceSim()
    sim1 = dissim.xmlSim(xml1, xml2)
    nlpProecss = NLPProcess()
    nodesim = NodeSim(nlpProecss)
    sim2, classList = nodesim.nodeSim(xml1, xml2)
    sim = round((sim1 + sim2) * 50, 2)
    print(sim1)
    print(sim2)
    print(sim)
    # 画图,结果存放于 /front_end/static/img/res.png
    base_image = os.path.join(os.getcwd(), 'front_end', 'storage', 'b.png')
    current_image = os.path.join(os.getcwd(), 'front_end', 'storage', 'd.png')
    with open(base_image, 'rb') as f:
        data = f.read()
        base_image = base64.b64encode(data)  # 得到 byte 编码的数据
    with open(current_image, 'rb') as f:
        data = f.read()
        current_image = base64.b64encode(data)
    ImageUtil.isCVTextMatch(base_image, current_image)
    return sim, classList


if __name__ == '__main__':
    a, b = xmlSim()