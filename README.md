# README #

## for the hack of HQ like game

1.尝试了tesseract.js，报错跑不通，项目从17年开始就没有人维护了，放弃
2.打算使用百度提供的ocr
3.使用百度提供的ocr，可以实现基本的文字识别，但是考虑到图像的识别
    范围中如果带上了顶部文字和底部弹幕的话，会导致识别出很多无关的结果，

- [x] 使用adb截图
    - 先考虑使用python 来执行adb指令进行截图 期望结果：能够按一个键就能够得到当时手机的截图
    - 对截图进习惯裁剪，得到题目区域大小的目标图片  期望结果：能够得到去除了顶部title和底部弹幕的图片
- [x] 对截图进行裁剪 ，得到目标图片
- [x] 对目标图片进行ocr分析，得到一个问题和三个选项

## 速度在3秒左右

### 早上对百万英雄进行了测试，发现几个问题

- [ ] 没有识别出问号，导致题目和答案没有分离开，目前的算法是根据问号来分开答案和问题的
- [x] 百度搜索后，需要对当页的内容中，关键词出现的频率进行统计，给出参考答案，考虑使用爬虫

### 今天再次测试，发现了按shell命令，再看手机，再盯着屏幕有点难受。。 2018.1.7
- [ ] 优化答题流程，考虑弄一个Python的图形界面，方便交互 
- [ ] 题目提供的答案可能是三个，也可能是四个，需要优化流程，目前只提供了3个答案的流程 
- [ ] 考虑"以下哪个是哺乳动物？" 这样的问题，这个需要先进行分词，再把问题和每个答案进行搜索，根据搜到的相关结果数量，来判断参考答案
    - 这里如果是否定问句，那么就选择搜索结果最少的那个，如果是肯定问句，那么就选择搜索结果最多的那个
- [x] 增加日志功能
- [x] 保存多个图片，减少写入时间
