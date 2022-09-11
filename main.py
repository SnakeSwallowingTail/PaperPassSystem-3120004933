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





if __name__ == '__main__':
    # 从命令行参数获取文件路径
    path_original = sys.argv[1]
    path_fixed = sys.argv[2]
    path_answer = sys.argv[3]

    # 根据文件路径打开文件
    f2 = open(path_fixed, 'r')
    f3 = open(path_answer, 'w')
