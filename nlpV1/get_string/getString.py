from ..descriptor_processes import XML
from ..descriptor_processes import text_pre_process


class ApproachDescriptors:
    default_columns = ['src_app', 'target_app', 'src_event_index', 'target_label',
                       'src_class', 'target_class', 'src_type', 'target_type', 'target_event_index']
    atm = ['text', 'id', 'content_desc', 'hint', 'atm_neighbor', 'file_name']
    craftdroid = ['text', 'id', 'content_desc', 'hint', 'parent_text', 'sibling_text', 'activity']
    union = ['text', 'id', 'content_desc', 'hint', 'parent_text', 'sibling_text', 'activity', 'atm_neighbor',
             'file_name']  # 并
    intersection = ['text', 'id', 'content_desc', 'hint']  # 交
    descriptors_dict = {'default': default_columns, 'atm': atm, 'craftdroid': craftdroid,
                        'union': union, 'intersection': intersection}
    all = set(atm + craftdroid)


def node2String(node):
    xmlProcess = XML.XmlProcess()
    nodeInfo = xmlProcess.getNodeDf(node)
    if nodeInfo is None:
        return ''
    # TODO: 这里先用class代替字符串
    # nodeString = nodeInfo['class']
    nodeString = ''
    for i in ApproachDescriptors.atm:
        if nodeInfo[i] is None:
            continue
        nodeString = nodeString + nodeInfo[i] + ' '
    return nodeString


def token2String(token):
    tmp = ''
    for i in token:
        tmp = tmp + i + ' '
    return tmp


def getNodeString(node):
    # nodeString = 'EZ Tip 100 Calculator200 is a ssHiBuddy th1230at allows + you to thanksButton'
    # print(nodeString)
    nodeString = node2String(node)
    token = text_pre_process.pre_process(nodeString)
    if len(token) == 0:
        return ''
    newString = token2String(token)
    # print(newString)
    return newString


def pre_process_string(nodeString):
    token = text_pre_process.pre_process(nodeString)
    if len(token) == 0:
        return ''
    newString = token2String(token)
    # print(newString)
    return newString


if __name__ == "__main__":
    file1 = "/Users/apple/Desktop/3.xml"
    file2 = "/Users/apple/Desktop/1.xml"
    file_o1 = open(file1)
    xml1 = file_o1.read()
    file_o2 = open(file2)
    xml2 = file_o2.read()
    find1 = {'className': 'android.widget.Button', 'instance': 0}
    find2 = {
        'xpath': '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[2]/android.support.v4.widget.DrawerLayout/android.widget.ListView/android.widget.TextView[4]'}
    # getXmlString(xml1, find1)
    # getXmlString(xml2, find2)
