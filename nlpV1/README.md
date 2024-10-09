# README

### `NLPProcess.py`

根目录下的`NLPProcess`为核心功能类，调用其函数`run(self,  src_string, target_string)`可以得到两个目标字符串的nlp相似度

调用其函数`runWithXml(self, xml1, find1, image1, xml2, find2, image2)`为模型使用的固定参数的调用函数



### `getString.py`

目录`get_string`下的`getString.py`为拓展模块，调用函数`getXmlString(xml, descriptor)`，其参数为string类型的xml文件和描述符（类似`find1 = {'className': 'android.widget.Button', 'instance': 0}`），可以得到相关节点根据nlp模型处理后得到的字符串，可使用此字符串调用`NLPProcess.py`中的函数



### 无效字符串的过滤

目录`descriptor_processes`下的`word_filter(token)`函数为过滤函数，在其中的列表 `filterWord`中添加过滤词即可