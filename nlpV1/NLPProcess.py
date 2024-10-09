import logging
import gensim.models.keyedvectors as word2vec
import os
# from .evaluators import evaluator_builder

from .evaluators import evaluator
from .get_string import getString

logging.basicConfig(level=logging.WARNING)


class NLPProcess:
    def __init__(self):
        model, Type = self.get_model_type()
        self.builder = evaluator.Evaluator(model, Type)
        # self.embedding = 'wm'
        # self.descriptor = 'atm'
        # self.algorithm = 'custom'
        # self.train_set = 'googleplay'
        # train_set = 'standard'
        # self.semantic_config = {"algorithm": self.algorithm, "descriptors": self.descriptor,
        #                         "training_set": self.train_set, 'word_embedding': self.embedding}

    def run(self, src_string, target_string, method):
        """
        计算相似度
        :param src_string: 未经预处理的字符串
        :param target_string: 未经预处理的字符串
        :param method: 'string' 代表句子匹配, 'token' 代表词组匹配
        :return:
        """
        self.builder.set_semantic_config()
        simResult = self.builder.assign_score(src_string, target_string, method)
        return simResult

    def get_model_type(self):
        model_path = os.path.join(os.getcwd(), 'nlpV1', 'embedding', 'w2v-googleplay.model')
        try:
            model = word2vec.KeyedVectors.load_word2vec_format(model_path, binary=True)
            Type = 1  # 不用加'.wv'
        except UnicodeDecodeError:
            model = word2vec.KeyedVectors.load(model_path)
            Type = 0  # 需要加'.wv'
        return model, Type

    # 模块调用的固定参数的函数
    # def runWithXml(self, xml1, image1, find1, xml2, image2, find2):
    #     string1 = getString.findNode(xml1, find1)
    #     string2 = getString.findNode(xml2, find2)
    #     # print(string1)
    #     # print(string2)
    #     self.builder.set_semantic_config()
    #     simResult = self.builder.assign_score(string1, string2)
    #     return simResult


if __name__ == "__main__":
    file1 = "/Users/apple/Desktop/4.xml"
    file2 = "/Users/apple/Desktop/11.xml"
    file_o1 = open(file1)
    xml1 = file_o1.read()
    file_o2 = open(file2)
    xml2 = file_o2.read()
    find1 = {'resourceId': 'com.kvannli.simonkvannli.dailybudget:id/button2'}
    find2 = {'className': 'android.widget.TextView', 'instance': 3}
    src_string = 'NON number'
    target_string = 'monthly number'
    # src_string = '   '
    # target_string = '100abcd'
    nlpProecss = NLPProcess()
    print(nlpProecss.run(src_string, target_string))
    # print(nlpProecss.runWithXml(xml1, None, find1, xml2, None, find2))
