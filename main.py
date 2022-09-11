import re
import jieba
import sys


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
        if re.match(u"[a-zA-Z0-9\u4e00-\u9fa5]", tags):  # 只将tags中的英文、数字、汉字保存进result中
            result.append(tags)
        else:
            pass
    return result


if __name__ == '__main__':
    # 从命令行参数获取文件路径
    path_original = sys.argv[1]
    path_fixed = sys.argv[2]
    path_answer = sys.argv[3]

    # 根据文件路径打开文件
    f2 = open(path_fixed, 'r')
    f3 = open(path_answer, 'w')
