"""
图片处理类
将两张截图上匹配的控件连线
"""
import cv2
import numpy as np
import base64
import time
from node_sim import NodeSim
from datebase import DateBase

# 非标准色，挑的是我喜欢的颜色
colorList = {
    'black': (0, 0, 0),
    'blue': (255, 255, 0),
    'green': (159, 255, 84),
    'gold': (0, 215, 255),
    'orange': (0, 165, 255),
    'grey': (130, 130, 130),
    'lawnGreen': (0, 252, 124),
    'orangeRed': (0, 69, 255)
}


class ImageUtil(object):
    @staticmethod
    def isCVTextMatch(image1, image2):
        image1 = base64.b64decode(image1)
        image2 = base64.b64decode(image2)

        # 数据流恢复成图像
        nparr1 = np.frombuffer(image1, np.uint8)
        img1 = cv2.imdecode(nparr1, cv2.IMREAD_COLOR)
        nparr2 = np.frombuffer(image2, np.uint8)
        img2 = cv2.imdecode(nparr2, cv2.IMREAD_COLOR)

        ImageUtil.explore_match(img1, img2)

    @staticmethod
    def reBounds(bounds1, bounds2):
        p1_x = int(bounds1.split(',')[0][1:])
        p1_y = int(bounds1.split(',')[1].split(']')[0])
        p2_x = int(bounds1.split(',')[1].split('[')[1])
        p2_y = int(bounds1.split(',')[2][0:-1])
        p3_x = int(bounds2.split(',')[0][1:])
        p3_y = int(bounds2.split(',')[1].split(']')[0])
        p4_x = int(bounds2.split(',')[1].split('[')[1])
        p4_y = int(bounds2.split(',')[2][0:-1])
        return p1_x, p1_y, p2_x, p2_y, p3_x, p3_y, p4_x, p4_y

    @staticmethod
    def explore_match(img1, img2):
        h1, w1 = img1.shape[:2]
        h2, w2 = img2.shape[:2]
        vis = np.zeros((max(h1, h2), w1 + w2, 3), np.uint8)
        vis[:h1, :w1, :] = img1
        vis[:h2, w1:w1 + w2, :] = img2

        db = DateBase()
        boundsList = db.readDb()
        cv2.line(vis, (w1, 0), (w1, max(h1, h2)), color=colorList['grey'], thickness=8)
        for d in boundsList:
            bounds1 = d['src']
            bounds2 = d['dst']
            p1_x, p1_y, p2_x, p2_y, p3_x, p3_y, p4_x, p4_y = ImageUtil.reBounds(bounds1, bounds2)
            cv2.rectangle(vis, (p1_x, p1_y), (p2_x, p2_y), color=colorList['lawnGreen'], thickness=4)
            cv2.rectangle(vis, (p3_x + w1, p3_y), (p4_x + w1, p4_y), color=colorList['lawnGreen'], thickness=4)
            cv2.line(vis, (p2_x, int((p1_y + p2_y) / 2)), (p3_x + w1, int((p3_y + p4_y) / 2)),
                     color=colorList['orangeRed'], thickness=3)

        img_file = 'front_end/static/img/res.png'
        cv2.imwrite(img_file, vis)


if __name__ == '__main__':
    base_image = "/Users/apple/Desktop/xml/3.png"
    current_image = "/Users/apple/Desktop/xml/0.png"
    with open(base_image, 'rb') as f:
        data = f.read()
        base_image = base64.b64encode(data)  # 得到 byte 编码的数据
    with open(current_image, 'rb') as f:
        data = f.read()
        current_image = base64.b64encode(data)  # 得到 byte 编码的数据
    file1 = "/Users/apple/Desktop/xml/3.xml"
    file_o1 = open(file1)
    xml1 = file_o1.read()
    file2 = "/Users/apple/Desktop/xml/0.xml"
    file_o2 = open(file2)
    xml2 = file_o2.read()
    ss = NodeSim()
    print(ss.nodeSim(xml1, xml2))
    ImageUtil.isCVTextMatch(base_image, current_image)
