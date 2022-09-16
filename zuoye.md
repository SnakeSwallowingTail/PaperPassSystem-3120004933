| <center>这个作业属于哪个课程     | <center>[广工软件工程课程学习](https://bbs.csdn.net/forums/gdut-ryuezh)     |
| :------------- | :------------- |
| <center>这个作业要求       | <center>[个人项目作业-论文查重](https://bbs.csdn.net/topics/608092799) |
| <center>这个作业的目标 | 按需求完成编码、进行测试并创建博客 |
| <center> github仓库链接 | <center>[代码仓库链接](https://github.com/SnakeSwallowingTail/PaperPassSystem-3120004933) |

<toc>

## PSP表格
| <center>PSP2.1|Personal Software Process Stages|预估耗时(min)|实际耗时(min)|
| :-------------| :----------------------------- |:-----------| :----------|
|**Planning**|**计划**|**10**|**15**|
|Estimate|估计这个任务需要多少时间|10|15|
|**Development**|**开发**|**185**|**110**|
|Analysis|需求分析 (包括学习新技术)|60|30|
|Design Spec|生成设计文档|15|10|
|Design Review|设计复审|15|10|
|Coding Standard|代码规范 (为目前的开发制定合适的规范)|10|5|
|Design|具体设计|30|15|
|Coding|具体编码|45|30|
|Code Review|代码复审|10|10|
|Test|测试（自我测试，修改代码，提交修改）|60|90|
|**Reporting**|**报告**|**40**|**50**|
|Test Report|测试报告|20|30|
|Size Measurement|计算工作量|10|10|
|Postmortem & Process Improvement Plan|事后总结, 并提出过程改进计划|10|10
||合计|235|175|

## 设计与实现

### 实现思路
查询网上已有文章，总结实现思路如下：

1. 将待处理的文章进行分词，得到存储若干词汇的列表
2. 计算并记录列表中词汇对应出现的次数，将这些次数存储于一个向量（词频表）中
3. 将不同文章对应的词频表带入夹角余弦定理
4. 将计算得到的余弦值看作文章的重复率

### 项目依赖
![requirement](D:\Courses\SE\PaperPassSystem-3120004933\requirement.png)

### 所用接口

jieba.cut
---
用于对中文句子进行分词，功能详见[Github说明文档](https://github.com/fxsjy/jieba)。

该方法提供多种分词模式供选择，这里仅使用默认最简单的“精确模式”。

re.match
---
由于对比的对象为中、英文词句，因此应过滤掉文件读取中的换行符`\n`以及标点符号。

本项目中采用正则表达式来匹配符合的数据。

gensim.dictionary.doc2bow
---
doc2bow是gensim中封装的一个方法，主要用于实现bow模型

> bag-of-words model (BoW model) 最早出现在自然语言处理(Natural Language Processing）和信息检索（Information Retrieval）领域.。该模型忽略掉文本的语法和语序等要素，将其仅仅看作是若干个词汇的集合，文档中每个单词的出现都是独立的。

gensim.similarities.Similarity
---
gensim中封装的一个方法，主要用于计算余弦相似度，具体实现方法gensim说明文档中未给出


sys.argv
---
用于存储命令行参数，以实现程序内对命令行参数的调用

os.path.exist
---
用于检测文本路径是否存在。若路径存在则返回True，否则返回False


### 关键函数
- **字符过滤函数char_filter**
```Python
def char_filter(str):
    str = jieba.lcut(str)  # jieba分词，直接返回list类型
    result = []
    for tags in str:
        if re.match(u'[a-zA-Z\d\u4e00-\u9fa5]', tags):  # 只将tags中的英文、数字、汉字保存进result中
            result.append(tags)
    return result
```
该函数用于对字符串进行分词、过滤。  
首先应用`jieba.lcut`进行分词，并用返回的list型对象（其中存储分词结果）覆盖原有字符串型对象。  
for循环实际上利用了list型对象的迭代器特性，程序按顺序从str(已变为list型对象)中选择元素，并判断该元素是否满足正则表达式，如果满足则插入至list型对象result中。最后返回的结果result就是包含分词结果的列表（未去重），且其中元素按文本顺序排列。

- **计算文章相似度函数calc_similarity**
```Python
def calc_similarity(text1, text2):
    texts = [text1, text2]
    dictionary = gensim.corpora.Dictionary(texts)  # 根据两篇文章的所有内容构建词表
    corpus = [dictionary.doc2bow(text) for text in texts]  # 记录词表中所有词的频率
    similarities = gensim.similarities.Similarity(None, corpus=corpus, num_features=len(dictionary))  # 参数为：碎片文件名路径(不管,在缓存中随机读取）、词频、字典大小
    cosine_sim = similarities[corpus[0]][1]  # 对文章一进行相似度查询
    cosine_sim = float("%.6f" % cosine_sim)
    return cosine_sim
```
该函数用于计算文章相似度。  
首先将对两篇文章分词好的结果（词表）插入到一个list型对象中，此时可以将texts这一list型对象看作一个广义表。随后利用gensim封装的Dictionary方法将texts对象中所有元素去重，形成一个集合。去重后，利用doc2bow方法对两个词表计算词频并存储在corpus中，这里corpus的存储结构为`list[list[tuple(int,int)]]`  
计算完词频后，利用Similarity方法计算余弦相似度，并将结果存储在`cosine_sim`中，保留六位小数后返回结果。

### 性能分析
![性能分析](D:\Courses\SE\PaperPassSystem-3120004933\调用、性能分析.png)  
由于主要调用的都是库中封装的函数，基本达到性能最大值，几乎没有优化空间

### 异常处理

本项目中含有四处异常处理，其中两处用于识别文件路径，另外两处用于判断文件是否为空。   
```Python
if not os.path.exists(path_original):
    print("[-]原版文章不存在，请检查文件路径！")
    exit(0)
if not os.path.exists(path_fixed):
    print("[-]抄袭版文章不存在，请检查文件路径！")
    exit(0)
...
if len(str_ori) == 0:
    print("[-]原版文章为空文件，请检查文件内容")
    exit(0)
if len(str_fix) == 0:
    print("[-]抄袭版文章为空文件，请检查文件内容")
    exit(0)
```

- 异常情况A：文件路径不存在
![文件路径不存在]()

- 异常情况B：文件为空文件
![文件为空文件]()

## 测试与覆盖率

### 测试
**重复率计算测试**  
```Python
import unittest
import main
class MyTestCase(unittest.TestCase):
    def test_something1(self):
        self.assertEqual(main.calc_similarity(['这是', '一个', '软件工程', '作业', '的', '测试用例'],   
        ['这是', '一个', '软件工程', '的', '测试用例']), 0.912871)
if __name__ == '__main__':
    unittest.main()
```
这里根据`calc_similarity`函数的工作原理，使用随意撰写的一组测试数据，构建向量计算余弦值。  
之所以随意撰写数据，是因为在`calc_similarity`中，程序会自动地将两个传入的分词结果构建成一个大词库并分别对词库中的所有词计算词频。也就是说，即使存在在A出现但B中没有出现的词，在B的词频表中也会含有这一词，其出现次数为0。因此便可以构建两个维度相同的向量，随后对两向量求夹角余弦即可。  
`self.assertEqual`函数需要传入两个参数，第一个是预测值，另一个是实际值，如果运行通过，则会显示`OK`  ，否则如下图所示  
![测试失败]("#center")  
根据参数内容，传入`calc_similarity`函数后，函数构建的词频结果是:  
[(这是,1),(一个,1),(软件工程,1),(作业,1),(的,1),(测试用例,1)]  
[(这是,1),(一个,1),(软件工程,1),(作业,0),(的,1),(测试用例,1)]  
写成向量形式:[1,1,1,1,1,1],[1,1,1,0,1,1]  
代入余弦定理计算得到的结果是0.912871（保留六位小数）  
运行结果如下图，说明程序功能实现正常  
![成功运行]("#center")  


### 覆盖率

![覆盖率总览](D:\Courses\SE\PaperPassSystem-3120004933\覆盖率.png)  
![覆盖率详细](D:\Courses\SE\PaperPassSystem-3120004933\覆盖率-B.png)  
从`覆盖率详细`图中可以看出，大部分代码均覆盖到，少部分未覆盖的为异常处理，属于正常情况。
