from abc import ABC, abstractmethod
import numpy as np

# from ..get_string import getString
from ..get_string import getString
from nltk import word_tokenize

practical_zero = 0.000001


class WordEmbedding(ABC):
    model = None
    sentence_level = False
    zeros = 0
    Type = 0  # 用来表示是Word2Vec还是KeyedVectors，从而判断用不用加'wv.'

    @abstractmethod
    def __init__(self, model, Type):
        pass

    def calc_sim(self, a, b, method):
        """
        计算相似度
        因为之前经过了预处理，因此这里就不重复操作了
        :param a: 未经预处理的字符串
        :param b: 未经预处理的字符串
        :param method: 'string' 代表句子匹配, 'token' 代表词组匹配
        :return:
        """
        # a = getString.pre_process_string(a)
        # b = getString.pre_process_string(b)
        if a == '' and b == '':
            return 1.0
        if a == '' or b == '':
            return 0.0
        score = self.calc_sim_by_model(a, b, method)
        if score < practical_zero and self.sentence_level:
            self.zeros += 1
        return score

    @abstractmethod
    def calc_sim_by_model(self, a, b, method):
        pass


class Wor2VecBase(WordEmbedding, ABC):
    def __init__(self, model, Type):
        super().__init__(model, Type)
        self.load_model(model, Type)

    def load_model(self, model, Type):
        self.model = model
        self.Type = Type


class WordMovers(Wor2VecBase):
    sentence_level = True

    def calc_sim_by_model(self, a, b, method):
        if method == 'string':
            token_a = a
            token_b = b
        elif method == 'token':
            token_a = word_tokenize(a)
            token_b = word_tokenize(b)
        else:
            return 0
        # print(token_a, token_b)
        # print(token_b)
        if self.Type == 1:
            score = self.model.wmdistance(token_a, token_b)
        else:
            score = self.model.wv.wmdistance(token_a, token_b)
        if score == np.inf:
            return 0
        return 1 / (1 + score)


model_cache = {}


def embedding_factory(model, Type) -> WordEmbedding:
    # 这里花的时间最长
    embedding_type_name = 'wm'
    train_set = 'googleplay'
    key = embedding_type_name + train_set
    if key in model_cache.keys():
        model_cache[key].zeros = 0
        return model_cache[key]
    else:
        model_cache.clear()
        model_tmp = WordMovers(model, Type)
        model_cache[key] = model_tmp
    return model_tmp
