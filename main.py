import os.path
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
def char_filter(str):
    str = jieba.lcut(str)  # jieba分词，直接返回list类型
    result = []
    for tags in str:
        if re.match(u'[a-zA-Z\d\u4e00-\u9fa5]', tags):  # 只将tags中的英文、数字、汉字保存进result中
            result.append(tags)
    return result


# 计算文章相似度
def calc_similarity(text1, text2):
    texts = [text1, text2]
    dictionary = gensim.corpora.Dictionary(texts)  # 根据两篇文章的所有内容构建词表
    corpus = [dictionary.doc2bow(text) for text in texts]  # 记录词表中所有词的频率
    similarities = gensim.similarities.Similarity(None, corpus=corpus, num_features=len(dictionary))  # 参数为：碎片文件名路径(不管,在缓存中随机读取）、词频、字典大小
    cosine_sim = similarities[corpus[0]][1]  # 对文章一进行相似度查询
    cosine_sim = float("%.6f" % cosine_sim)
    return cosine_sim


if __name__ == '__main__':
    """
    if len(sys.argv) < 4:  # 判断命令行参数是否出错
        print("[-]参数数目错误，请检查参数")
        print("[-]python main.py绝对路径 原版文章绝对路径 抄袭版文章绝对路径 结果保存绝对路径")
        exit(0)
    # 从命令行参数获取文件路径r
    path_original = sys.argv[1]
    path_fixed = sys.argv[2]
    path_answer = sys.argv[3]
    """
    # 测试时直接采用绝对路径，不使用命令行传参
    # 正式运行时注释以下三行并将上方注释取消
    path_original = "D:/Courses/SE/PaperPassSystem-3120004933/测试文本-Beta/orig_d.txt"
    path_fixed = "D:/Courses/SE/PaperPassSystem-3120004933/测试文本-Beta/orig_d_dis.txt"
    path_answer = "D:/Courses/SE/PaperPassSystem-3120004933/ans.txt"

    # 查询文件是否存在
    if not os.path.exists(path_original):
        print("[-]原版文章不存在，请检查文件路径！")
        exit(0)
    if not os.path.exists(path_fixed):
        print("[-]抄袭版文章不存在，请检查文件路径！")
        exit(0)
    # 终端显示文件路径
    print("[+]原版文章的绝对路径:{0}".format(path_original))
    print("[+]抄袭版文章的绝对路径:{0}".format(path_fixed))
    # 读取文本
    str_ori = get_content(path_original)
    str_fix = get_content(path_fixed)
    # 检查是否存在空文本
    if len(str_ori) == 0:
        print("[-]原版文章为空文件，请检查文件内容")
        exit(0)
    if len(str_fix) == 0:
        print("[-]抄袭版文章为空文件，请检查文件内容")
        exit(0)
    # 终端显示文本内容
    print("[+]原版文章内容:\n{0}".format(str_ori))
    print("[+]抄袭版文章内容:\n{0}".format(str_fix))
    # 进行分词
    text_ori = char_filter(str_ori)
    text_fix = char_filter(str_fix)
    # 终端显示分词结果
    print("[+]原版文章分词结果:{0}\n".format(text_ori))
    print("[+]抄袭版文章分词结果:{0}\n".format(text_fix))
    # 计算相似度
    similarity = calc_similarity(text_ori, text_fix)
    # 存储相似度结果
    fout = open(path_answer, 'w')
    fout.write("文章相似度:{0:.6f}".format(similarity))
    fout.close()
    # 终端显示运行结束
    print("文章相似度:{0:.6f}".format(similarity))
    print("[+]计算完成，结果已保存至{0}".format(path_answer))
    print("[+]运行结束")
