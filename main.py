import re
import sys

import gensim.corpora
import jieba


# 从路径获取文本内容
def get_content(path):
    str = ''
    f = open(path, 'r', encoding='UTF-8')
    line = f.readline()
    while line:
        str = str + line
        line = f.readline()
    f.close()
    return str


# jieba分词并过滤标点符号等
def filter(str):
    str = jieba.lcut(str)  # 直接返回list类型
    result = []
    for tags in str:
        if re.match(u"[a-zA-Z\d\u4e00-\u9fa5]", tags):  # 只将tags中的英文、数字、汉字保存进result中
            result.append(tags)
        else:
            pass
    return result


# 计算文章相似度
def calc_similarity(text1, text2):
    texts = [text1, text2]
    dictionary = gensim.corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]
    similarity = gensim.similarities.Similarity('-Similarity-index', corpus, num_features=len(dictionary))
    test_corpus = dictionary.doc2bow(text1)
    cosine_sim = similarity[test_corpus][1]
    return cosine_sim


if __name__ == '__main__':
    # 从命令行参数获取文件路径r
    path_original = sys.argv[1]
    path_fixed = sys.argv[2]
    path_answer = sys.argv[3]
    str_ori = get_content(path_original)
    str_fix = get_content(path_fixed)
    text1 = filter(str_ori)
    text2 = filter(str_fix)
    similarity = calc_similarity(text1, text2)
    f = open(path_answer, 'w')
    f.write('文章相似度:{0:.4f}'.format(similarity))
    f.close()
