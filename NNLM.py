# %%
# code by Tae Hwan Jung @graykode
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np


def make_batch():
    input_batch = []
    target_batch = []
    max_len = 0

    for sen in sentences:
        word = sen.split()  # space tokenizer
        max_len = len(word) if len(word) > max_len else max_len
        input = [word_dict[n] for n in word[:-1]]  # create (1~n-1) as input
        target = word_dict[word[-1]]  # create (n) as target, We usually call this 'casual language model'

        input_batch.append(input)
        target_batch.append(target)

    return input_batch, target_batch, max_len


# Model
class NNLM(nn.Module):
    def __init__(self):
        super(NNLM, self).__init__()
        self.C = nn.Embedding(n_class, m)
        self.H = nn.Linear(n_step * m, n_hidden, bias=False)
        self.d = nn.Parameter(torch.ones(n_hidden))
        self.U = nn.Linear(n_hidden, n_class, bias=False)
        self.W = nn.Linear(n_step * m, n_class, bias=False)
        self.b = nn.Parameter(torch.ones(n_class))

    def forward(self, X):
        X = self.C(X)  # X : [batch_size, n_step, m]
        X = X.view(-1, n_step * m)  # [batch_size, n_step * m]
        tanh = torch.tanh(self.d + self.H(X))  # [batch_size, n_hidden]
        output = self.b + self.W(X) + self.U(tanh)  # [batch_size, n_class]
        return output


if __name__ == '__main__':
    # sentences = ["i like dog", "i love coffee", "i hate milk"]
    sentences = []
    f = open('abc.txt', "r", encoding='utf-8')
    line = f.readline()  # 读取第一行
    while line:
        line = line.replace('\n', '')
        sentences.append(line)  # 列表增加
        line = f.readline()  # 读取下一行

    word_list = " ".join(sentences).split()
    word_list = list(set(word_list))
    word_dict = {w: i for i, w in enumerate(word_list)}
    number_dict = {i: w for i, w in enumerate(word_list)}
    n_class = len(word_dict)  # number of Vocabulary

    input_batch, target_batch, max_len = make_batch()
    tmp_batch = []
    for line in input_batch:
        line = np.pad(line, (0, max_len - 1 - len(line)), 'constant', constant_values=(0, 0))
        tmp_batch.append(line)

    n_step = max_len - 1  # n-1 in paper, look back n_step words and predict next word. In this task n_step=2
    n_hidden = 2  # h in paper
    m = 2  # m in paper, word embedding dim

    input_batch = torch.LongTensor(np.array(tmp_batch))
    target_batch = torch.LongTensor(target_batch)

    model = NNLM()

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    # Training
    for epoch in range(5000):
        optimizer.zero_grad()
        output = model(input_batch)
        # print(output)

        # output : [batch_size, n_class], target_batch : [batch_size]
        loss = criterion(output, target_batch)
        if (epoch + 1) % 1000 == 0:
            print('Epoch:', '%04d' % (epoch + 1), 'cost =', '{:.6f}'.format(loss))

        loss.backward()
        optimizer.step()

    # Predict
    predict = model(input_batch).data.max(1, keepdim=True)[1]
    print(predict)

    # Test
    print([sen.split()[:len(sen) - 1] for sen in sentences], '->', [number_dict[n.item()] for n in predict.squeeze()])

    torch.save(model, 'nnlm.pt')
