from ..embedding import word_embedding


def extract_threshold(algorithm: str):
    number = int(algorithm.split('_')[1])
    return number / 100


class Evaluator:
    def __init__(self, model, Type):
        self._semantic_config = {'word_embedding': None, 'training_set': None, 'algorithm': None,
                                 'descriptors': None}
        self.model = model
        self.Type = Type
        self.technique = None

    # 加载模型
    def set_semantic_config(self):
        self.technique = word_embedding.embedding_factory(self.model, self.Type)

    # 核心函数：计算两个string的相似度
    def assign_score(self, src_string, target_string, method):
        return self.technique.calc_sim(src_string, target_string, method)
