import re
import sys

import gensim.corpora
import jieba


# 从路径获取文本内容
def get_content(path):
    str = ''
    f = open(path, 'r', encoding='UTF-8')  # 打开文件
    line = f.readline()  # 读取当前行并下移光标
    while line:
        str = str + line  # 拼接文本
        line = f.readline()  # 读取当前行并下移光标
    f.close()
    return str  # 返回读取后的文本并保存在内存中


# jieba分词并过滤标点符号等
def filter(str):
    str = jieba.lcut(str)  # jieba分词，直接返回list类型
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
    dictionary = gensim.corpora.Dictionary(texts)  # 根据两篇文章的所有内容构建词表
    corpus = [dictionary.doc2bow(text) for text in texts]  # 记录词表中所有词的频率
    similarity = gensim.similarities.Similarity(None, corpus=corpus, num_features=len(dictionary))  # 参数为：碎片文件名路径(不管,在缓存中随机读取）、词频、字典大小
    test_corpus = dictionary.doc2bow(text1)  # 文章一中所有词在词表中的出现频率
    cosine_sim = similarity[test_corpus][1]  # 对文章一进行相似度查询
    return cosine_sim


if __name__ == '__main__':
    # 从命令行参数获取文件路径r
    path_original = sys.argv[1]
    path_fixed = sys.argv[2]
    path_answer = sys.argv[3]
    str_ori = get_content(path_original)
    str_fix = get_content(path_fixed)
    text_ori = filter(str_ori)
    text_fix = filter(str_fix)
    similarity = calc_similarity(text_ori, text_fix)
    f = open(path_answer, 'w')
    f.write('文章相似度:{0:.6f}'.format(similarity))
    f.close()
