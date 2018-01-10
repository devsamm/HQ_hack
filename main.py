# -*- coding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8') 
from aip import AipOcr
import os
from PIL import Image
from logger import Log
from io import BytesIO
import re
import webbrowser
import urllib
import urllib2
import collections
from bs4 import BeautifulSoup
import time

# 每一次运行，都保存独立的日志，根据题目名称来保存
# 每个题目为单独一个文件夹，包含详细日志文件以及截图文件，截图文件用时间命名，比如20180107120432.png。


APP_ID = '10643473'
API_KEY = 'N6qbo65qp120AAHHDralAKDD'
SECRET_KEY = 'aKFHazKri9DmWYoE3zGWFstU6Hv9vMlg'
# 冲顶大会截图剪切范围配置
CDDH_CONFIG = (0,312,1080,1166)
# 创建日志文件夹
name = time.strftime("%Y%m%d%H%M%S", time.localtime()) 
dirPath = './log/'+name
os.mkdir(dirPath)

log = Log(dirPath)



def getTimeNow():
    return time.time()

timeInit = getTimeNow()
log.record('开始生成流程...',False)
client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
os.popen('adb shell screencap -p   >  ~/Documents/hq_auto/hq_auto/log/'+name+'/'+name+'.png')
# 这里需要停300ms，防止图片还未生成
time.sleep(0.2)
log.record('adb拉取截图完毕，耗费时间:' + str(int(getTimeNow() - timeInit))+'ms' ,False)
im = Image.open('./log/'+name+'/'+name+'.png')
box = CDDH_CONFIG
final_image = im.crop(box)

outputBuffer = BytesIO()
final_image.save(outputBuffer,format='PNG')
log.record('图片处理完成，耗费时间：'+str(int(getTimeNow() - timeInit))+'ms',False)
# 这里最好还是使用精确模式
result = client.basicAccurate(outputBuffer.getvalue());
log.record(result,False)
log.record('OCR识别完成，耗费时间：'+str(int(getTimeNow() - timeInit))+'ms',False)  
question = ''
answerA = ''
answerB = ''
answerC = ''
for (key,name) in result.items():
    if(key == 'words_result'):
        for item in name:
            word = item['words']
            if not  '?' in question:
                question = question + word
            elif not answerA:
                answerA = word
            elif not answerB:
                answerB = word
            else:
                answerC = word
            
#  需要把题目前面的数字去掉
question = re.sub('^\d{1,2}\.?','',question)
question_encode = urllib.urlencode([('w',question)])
url = 'http://www.baidu.com/s?'+question_encode
log.record('打开的url是：'+url,False)
webbrowser.open_new(url)
log.record('调用浏览器打开，共耗费时间:'+str(int(getTimeNow() - timeInit))+'ms',False)
log.record('问题是：'+question,True)
log.record('答案A是：'+answerA,True)
log.record('答案B是：'+answerB,True)
log.record('答案C是：'+answerC,True)

# 获取搜索结果，进行关键词分析
html_response = urllib2.urlopen(url)
html_content = html_response.read()
result_html = BeautifulSoup(html_content,'lxml')
result =  result_html.find("div", id="content_left")
# 取得百度第一页搜索结果的所有文本
final_result = result.get_text()
a_counts = final_result.count(answerA)
b_counts = final_result.count(answerB)
c_counts = final_result.count(answerC)
log.record('A答案出现次数：'+str(a_counts)+'次',False)
log.record('B答案出现次数：'+str(b_counts)+'次',False)
log.record('C答案出现次数：'+str(c_counts)+'次',False)

# 根据出现频率算出最后结果
answer = ''
if a_counts > b_counts:
    if a_counts >c_counts:
        answer = 'A'
    else:
        answer = 'C'
else:
    if b_counts>c_counts:
        answer = 'B'
    else:
        answer = 'C'
if a_counts == 0 and b_counts == 0 and c_counts == 0:
    answer = '祝你好运，瞎猜一个吧'

log.record('参考答案是:'+answer,True)








        
            

