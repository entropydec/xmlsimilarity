# encoding=utf-8
import logging
import lxml.etree

logger = logging.getLogger("meter")

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET


class XmlProcess:
    def __init__(self):
        self.classDic = {}
        self.idDic = {}
        self.descriptDic = {}
        self.textDic = {}

        self.childNodeRes = []
        self.parentNodeRes = []

    def getRoot(self, xmlFile):
        xmlFile = xmlFile.replace("&", "")
        xmlFile = xmlFile.replace("#", "")
        tree = ET.fromstring(xmlFile)  # <class 'xml.etree.ElementTree.ElementTree'>
        # 获取根节点 <Element 'data' at 0x02BF6A80>
        self.delete_system_node(tree)
        return tree

    @staticmethod
    def isCover(bounds1, bounds2):
        p1_x = int(bounds1.split(',')[0][1:])
        p1_y = int(bounds1.split(',')[1].split(']')[0])
        p2_x = int(bounds1.split(',')[1].split('[')[1])
        p2_y = int(bounds1.split(',')[2][0:-1])
        p3_x = int(bounds2.split(',')[0][1:])
        p3_y = int(bounds2.split(',')[1].split(']')[0])
        p4_x = int(bounds2.split(',')[1].split('[')[1])
        p4_y = int(bounds2.split(',')[2][0:-1])
        if p1_x <= p3_x and p1_y <= p3_y and p2_x >= p4_x and p2_y >= p4_y:
            return 1
        else:
            return 0

    # 删除有覆盖部分的下层部分的节点
    def remove_cover(self, root):
        childList = list(root)
        if len(childList) > 1:
            for i, child in enumerate(childList[:]):
                i = childList.index(child)
                for child2 in childList[0:i][:]:
                    if len(child) == 0 and len(child2) != 0:  # 叶子节点不能删除容器节点，但是能删除叶子节点
                        continue
                    if self.isCover(child2.get('bounds'), child.get('bounds')):
                        root.remove(child2)
                        # print('123456')
                        childList.remove(child2)
        for child in root:
            self.remove_cover(child)

    # 删除系统控件
    def delete_system_node(self, root):
        for child in list(root)[:]:
            if child.get('package') == 'com.android.systemui' and (
                    child.get('class') == 'android.widget.LinearLayout'
                    or child.get('class') == 'android.widget.FrameLayout'):
                root.remove(child)
            else:
                for grand_child in list(child)[:]:
                    if grand_child.get('class') == 'android.view.View' and (
                            grand_child.get('resource-id') == 'android:id/statusBarBackground' or grand_child.get(
                            'resource-id') == 'android:id/navigationBarBackground'):
                        child.remove(grand_child)
        self.remove_cover(root)

    def initIDDic(self):
        self.classDic = {}
        self.idDic = {}
        self.descriptDic = {}
        self.textDic = {}

    # 对xml进行重写，把默认xml的index重写为脚本中的索引index ，保存在本地的字典里
    def denoteCurrentXmlIndex(self, root):
        if 'class' in list(root.keys()):
            try:
                if 'bounds' in root.attrib:
                    root.set('x', int(root.attrib['bounds'].split(',')[0][1:]))
                    root.set('y', int(root.attrib['bounds'].split(',')[1].split(']')[0]))
                    root.set('w', int(root.attrib['bounds'].split(',')[1].split('[')[1]) - root.attrib['x'])
                    root.set('h', int(root.attrib['bounds'].split(',')[2][0:-1]) - root.attrib['y'])
                else:
                    if 'width' in root.attrib and 'height' in root.attrib:
                        root.set('x', 0)
                        root.set('y', 0)
                        root.set('w', int(root.attrib['width']))
                        root.set('h', int(root.attrib['height']))
                        root.set('bounds',
                                 '[0,0][' + str(root.attrib['width']) + ',' + str(root.attrib['height']) + ']')
                    else:
                        root.set('x', 0)
                        root.set('y', 0)
                        root.set('w', 0)
                        root.set('h', 0)
                        root.set('bounds', '[0,0][0,0]')
            except:
                logger.info("bounds of elements should be examined.")

            if root.attrib['class'] not in list(self.classDic.keys()):
                self.classDic[root.attrib['class']] = 1
            else:
                self.classDic[root.attrib['class']] = self.classDic[root.attrib['class']] + 1

            # 重写index
            root.set('classIndex', self.classDic[root.attrib['class']] - 1)

            if 'resource-id' in root.attrib and root.attrib['resource-id'] != '':
                if 'android:id/' in root.attrib['resource-id']:
                    root.set('id', '')
                else:
                    root.set('id', root.attrib['resource-id'].split('/')[-1])
            else:
                root.set('id', '')

            if 'resource-id' in root.attrib and 'com.tencent.mm:id' in root.attrib['resource-id']:
                if root.attrib['resource-id'] not in list(self.idDic.keys()):
                    self.idDic[root.attrib['resource-id']] = 1
                else:
                    self.idDic[root.attrib['resource-id']] = self.idDic[root.attrib['resource-id']] + 1
                root.set('idIndex', self.idDic[root.attrib['resource-id']] - 1)

            # android:id type by android system
            if 'resource-id' in root.attrib and 'com.tencent.mm:id' not in root.attrib['resource-id']:
                if root.attrib['resource-id'] not in list(self.idDic.keys()):
                    self.idDic[root.attrib['resource-id']] = 1
                else:
                    self.idDic[root.attrib['resource-id']] = self.idDic[root.attrib['resource-id']] + 1
                root.set('idIndex', self.idDic[root.attrib['resource-id']] - 1)

            if 'content-desc' in root.attrib:
                if root.attrib['content-desc'] not in list(self.descriptDic.keys()):
                    self.descriptDic[root.attrib['content-desc']] = 1
                else:
                    self.descriptDic[root.attrib['content-desc']] = self.descriptDic[root.attrib['content-desc']] + 1
                root.set('content-descIndex', self.descriptDic[root.attrib['content-desc']] - 1)
            else:
                root.set('content-desc', '')

            if 'text' in root.attrib:
                if root.attrib['text'] not in list(self.textDic.keys()):
                    self.textDic[root.attrib['text']] = 1
                else:
                    self.textDic[root.attrib['text']] = self.textDic[root.attrib['text']] + 1
                root.set('textIndex', self.textDic[root.attrib['text']] - 1)
            else:
                root.set('text', '')

            if 'semantic_rep' not in root.attrib:
                root.set('semantic_rep', '')
            if 'file_name' not in root.attrib:
                root.set('file_name', '')
            if 'EditText' in root.get('class'):
                root.set('type', 'fillable')
            else:
                root.set('type', 'clickable')
            if 'hint' not in root.attrib:
                root.set('hint', '')
            if 'parent_text' not in root.attrib:
                root.set('parent_text', '')
            if 'fillable_neighbor' not in root.attrib:
                root.set('sibling_text', '')
            if 'neighbors' not in root.attrib:
                root.set('neighbors', '')
            if 'activity' not in root.attrib:
                root.set('activity', '')
            if 'atm_neighbor' not in root.attrib:
                root.set('atm_neighbor', '')
        # print root.attrib
        for child in root:
            child.set('parent', root)
            self.denoteCurrentXmlIndex(child)

    def getChildNodeList(self, root):
        hasChild = False
        for child in root:
            hasChild = True
            self.getChildNodeList(child)

        if not hasChild:
            # avoid the case that listview contains no child widget, but denoted as a child widget.
            listTypeList = ['android.widget.ListView', 'android.support.v7.widget.RecyclerView', 'android.view.View',
                            'android.widget.GridView']
            if root.get('class') not in listTypeList:
                if (root.get('w') >= 30 and root.get('h') >= 30) or root.get('text') != '':
                    self.childNodeRes.append(root)
            elif root.get('class') == 'android.view.View' and (
                    root.get('text') != '' or root.get('content-desc') != '' or root.get('resource-id') != ''):
                self.childNodeRes.append(root)

    def getParentNodeList(self, root):
        hasChild = False
        for child in root:
            hasChild = True
            self.getParentNodeList(child)

        if not hasChild:
            # avoid the case that listview contains no child widget, but denoted as a child widget.
            listTypeList = ['android.widget.ListView', 'android.support.v7.widget.RecyclerView',
                            'android.widget.GridView']
            if root.get('class') in listTypeList:
                self.parentNodeRes.append(root)
        else:
            self.parentNodeRes.append(root)

    def getTree(self, xml):
        oldRoot = self.getRoot(xml)
        # 对根节点进行预处理
        oldRoot.set('class', 'hierarchy')

        # 对xml进行重写，把默认xml的index重写为脚本中的索引index ，保存在本地的字典里
        self.denoteCurrentXmlIndex(oldRoot)
        self.initIDDic()
        return oldRoot

    def rename(self, root):
        if 'class' in root.attrib:
            root.tag = root.get('class')
        for child in root:
            self.rename(child)

    def getNodeDf(self, node):
        if node is None:
            return None
        nodeInfo = {'id': node.get('id'), 'text': node.get('text'),
                    'file_name': node.get('file_name'),
                    'class': node.get('class'), 'type': node.get('type'),
                    'content_desc': node.get('content-desc'), 'hint': node.get('hint'),
                    'atm_neighbor': node.get('atm_neighbor')}
        return nodeInfo

    def getNode(self, find, nodeList, file):
        if find is None:
            return None
        if list(find.keys())[0] == 'resourceId':
            for node in nodeList:
                if node.get('resource-id') == list(find.values())[0]:
                    return node
        elif list(find.keys())[0] == 'description':
            for node in nodeList:
                if node.get('content-desc') == list(find.values())[0]:
                    return node
        elif list(find.keys())[0] == 'xpath':
            newtree = lxml.etree.fromstring(file)
            self.rename(newtree)
            newroot = newtree.xpath(list(find.values())[0])
            if len(newroot) == 0:
                return None
            for node in nodeList:
                if node.get('class') == newroot[0].get('class') and node.get('bounds') == newroot[0].get('bounds'):
                    return node
        elif list(find.keys())[0] == 'className':
            for node in nodeList:
                if node.get('class') == list(find.values())[0] and node.get('classIndex') == int(
                        list(find.values())[1]):
                    return node
        elif list(find.keys())[0] == 'textMatches':
            wordList = list(find.values())[0].split('|')
            for word in wordList:
                for node in nodeList:
                    if 'text' in node.attrib and word in node.get('text'):
                        return node
                    elif 'resource-id' in node.attrib and word in node.get('resource-id'):
                        return node
                    elif 'content-desc' in node.attrib and word in node.get('content-desc'):
                        return node
                    elif 'hint' in node.attrib and word in node.get('hint'):
                        return node
                    elif 'file-name' in node.attrib and word in node.get('file-name'):
                        return node
                    elif 'activity-name' in node.attrib and word in node.get('activity-name'):
                        return node
        return None


if __name__ == '__main__':
    file1 = "/Users/apple/Desktop/0.xml"
    file2 = "/Users/apple/Desktop/1.xml"
    file_o1 = open(file1)
    xml1 = file_o1.read()
    file_o2 = open(file2)
    xml2 = file_o2.read()
    find1 = {'description': 'Open navigation drawer'}
    find2 = {'resourceId': 'com.android.permissioncontroller:id/continue_button'}
    # find1 = {'description': 'Up'}
    # find2 = {'description': 'Up'}
    xmlProcess = XmlProcess()
    score = xmlProcess.getMatchingDf(xml1, find1)
