# PaperPassSystem-3120004933
## MISSION URL:[个人项目作业-论文查重](https://bbs.csdn.net/topics/608092799)
题目描述：

设计一个论文查重算法，给出一个原文文件和一个在这份原文上经过了增删改的抄袭版论文的文件，在答案文件中输出其重复率。

- 原文示例：今天是星期天，天气晴，今天晚上我要去看电影。
- 抄袭版示例：今天是周天，天气晴朗，我晚上要去看电影。
要求输入输出采用文件输入输出，规范如下：

- 从**命令行参数**给出：论文原文的文件的**绝对路径**。
- 从**命令行参数**给出：抄袭版论文的文件的**绝对路径**。
- 从**命令行参数**给出：输出的答案文件的**绝对路径**。

我们提供一份[样例](https://pan.baidu.com/s/1nONb0goQYtJVR4NxmfEB9Q?pwd=fjg7)，使用方法是：orig.txt是原文，其他orig_add.txt等均为抄袭版论文。

注意：答案文件中输出的答案为浮点型，精确到小数点后两位

## 实现思路

查询网上已有文章，总结实现思路如下：

1. 将待处理的文章进行分词，得到存储若干词汇的列表
2. 计算并记录列表中词汇对应出现的次数，将这些次数存储于一个向量中
3. 将不同文章对应的向量带入夹角余弦定理
4. 将计算得到的余弦值看作文章的重复率

## 开发工具

- IDE：JetBrain Pycharm 2022.1.1
- 所用语言：Python 3.10
- 第三方库：`jieba`、`gensim`

### 所用接口

jieba.cut
---
用于对中文句子进行分词，功能详见[Github](https://github.com/fxsjy/jieba)。

该方法提供多种分词模式供选择，这里只需用到默认最简单的“精确模式”。

re.match
---
由于对比的对象为中文或英文单词，因此应过滤掉文件读取中的换行符`\n`以及标点符号。

本项目中采用正则表达式来匹配符合的数据。

gensim.dictionary.doc2bow
---
doc2bow是gensim中封装的一个方法，主要用于实现bow模型

> bag-of-words model (BoW model) 最早出现在自然语言处理(Natural Language Processing）和信息检索（Information Retrieval）领域.。该模型忽略掉文本的语法和语序等要素，将其仅仅看作是若干个词汇的集合，文档中每个单词的出现都是独立的。

sys.argv
---
用于存储命令行参数，以实现程序内对命令行参数的调用
