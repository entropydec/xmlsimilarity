import re
import ssl
import string

import nltk
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize


def download_nltk_packages():
    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        pass
    else:
        ssl._create_default_https_context = _create_unverified_https_context
    nltk.download('omw-1.4')
    nltk.download('stopwords')
    nltk.download('averaged_perceptron_tagger')
    nltk.download('punkt')
    nltk.download('wordnet')


def remove_punctuation(s):
    translator = str.maketrans(string.punctuation, ' ' * len(string.punctuation))
    return s.translate(translator)


def remove_stop_words(input_str):
    stop_words = set(stopwords.words('english'))
    tokens = word_tokenize(input_str)
    result = [i for i in tokens if i not in stop_words]
    joined_result = ' '.join(result)
    if joined_result == '':
        return input_str
    else:
        return joined_result


def get_wordnet_pos(word):
    tag = nltk.pos_tag([word])[0][1][0].upper()
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}
    return tag_dict.get(tag, wordnet.NOUN)


def lemmatizing(input_str):
    lemmatizer = WordNetLemmatizer()
    input_str = word_tokenize(input_str)
    result = [lemmatizer.lemmatize(i, get_wordnet_pos(i)) for i in input_str]
    return ' '.join(result)


def token_camel_case_split(str):
    words = [[str[0]]]
    for c in str[1:]:
        if words[-1][-1].islower() and c.isupper():
            words.append(list(c))
        else:
            words[-1].append(c)
    return ' '.join([''.join(word) for word in words])


def camel_case_split(identifier):
    tokens = word_tokenize(identifier)
    result = []
    for i in tokens:
        result.append(token_camel_case_split(i))
    return ' '.join(result)


def remove_redundant_words(input_str):
    l = input_str.split()
    result = []
    for i in l:
        if input_str.count(i) > 1 and (i not in result) or input_str.count(i) == 1:
            result.append(i)
    return ' '.join(result)


def remove_unusual_char(input_str):
    return re.sub('[^A-Za-z0-9 ]+', '', input_str)


def space_cleaner(input_str):
    return ' '.join(str(input_str).split())


def word_segmentation(input_str):  # 按照小驼峰命名法分割单词
    token = []
    token_number = re.findall('[0-9]+', input_str)
    if input_str.isdigit():
        # 替换为number
        token.append('number')
        return token
    if input_str.isalpha():
        if input_str.islower() or input_str.isupper():
            token.append(input_str)
            return token
    token_word = re.findall('[a-zA-Z][a-z]+', input_str)
    dis = 0
    if len(token_number) == 0:
        return token_word
    if input_str.find(token_number[0]) == 0:
        token_word.insert(0, 'number')
        dis += len(token_number[0])
    for i in token_number:
        for j in token_word:
            dis += len(j)
            if dis == input_str.find(i):
                # 替换为number
                token_word.insert(token_word.index(j) + 1, 'number')
                dis += len(i)
    return token_word


# 过滤掉无效单词
def word_filter(token):
    filterWord = ['fab', 'iv', 'btn', 'button', 'tv', 'et', 'text', 'fsdf', 'tabhost', 'excluir']
    for word in filterWord:
        if word in token:
            token.remove(word)


def pre_process(input_str):
    token_word = []
    token_number = []
    if input_str == '' or input_str is None:
        return []
    token1 = word_tokenize(input_str)

    for s in token1:
        token_word += word_segmentation(s)
    all_token = []
    for s in token_word:
        s = s.lower()
        s = re.sub(r'\d+', '', s)
        s = remove_punctuation(s)
        s = s.strip()
        s = space_cleaner(s)
        s = remove_stop_words(s)
        s = lemmatizing(s)
        s = remove_unusual_char(s)
        all_token += word_tokenize(s)
    all_token += token_number
    word_filter(all_token)
    # print(all_token)
    return all_token


if __name__ == "__main__":
    # download_nltk_packages()
    # d = {'col1': ['ssHiBuddy hi isn\'t', 'input_note	45	Note (Optional) EZ',
    #               ' services saved required thinking allows developed',
    #               'EZ Tip Calculator is a ssHiBuddy simple tip calculator that allows you to specify the percent you'
    #               ' wish to tip'
    #               ' and the bill amount. This tip calculator is designed to calculate the tip quickly.']}
    # df = pd.DataFrame(data=d)
    # data = pre_process(df, True)
    # print(data)
    # print('download is completed.')
    print(pre_process('ADD INCOME btn_add_income'))
