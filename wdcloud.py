########用dic過濾API找到出現最多次數的詞語,並輸出文字雲(以政黑板為例)#####
#######可以優化的:辭典可以加權限#####



import json
import matplotlib.pyplot as plt
import jieba.posseg as pseg 
from wordcloud import WordCloud
#from udicOpenData.dictionary import *##助教給的dictionary,後來沒用因為很醜
from PIL import Image
import jieba
import jieba.posseg as pseg
import numpy as np
from collections import Counter
import time
now = int(time.time())                    ###current time stamp, precision to second
early = now - 1000000                      ###one day ago
str_now=str(now)                          ###轉成str
str_early=str(early)
print(str_early)
print(str_now)
struct_time = time.localtime(now) # 轉成時間元組
timeString = time.strftime("%Y-%m-%d", struct_time)
search_word="政治"
import requests
r = requests.get("https://ptt.nlpnchu.org/api/GetByContent?content="+search_word+"&start="+str_early+"&end="+str_now,verify=False)
list_of_dicts = r.json()
len = list_of_dicts['total']['value']
num=int(len/30)+1
remainder=len%30
print(remainder)
print(num)
print(len)
papers = " "
for j in range(num):
    strj=str(j)
    r = requests.get("https://ptt.nlpnchu.org/api/GetByContent?content="+search_word+"&start="+str_early+"&end="+str_now+"&size=30&from="+strj,verify=False)
    list_of_dicts = r.json()
    for i in range(30):
        if j == num-1 and i >= remainder:
            break
        dict1=list_of_dicts["hits"][i]
        article_title=dict1['_source']['article_title']
        content=dict1['_source']['content']
        papers=papers+article_title+content
jieba.set_dictionary('2021-10-12 dict.txt.big.txt')
#print("lalala")
jieba.add_word('柯文哲 99 n')
jieba.add_word('陳時中 99 n')
jieba.add_word('張亞中 99 n')
jieba.add_word('朱立倫 99 n')
jieba.add_word('國民黨 99 n')
jieba.add_word('民眾黨 99 n')
jieba.add_word('民進黨 99 n')
jieba.add_word('台灣 99 n')
jieba.add_word('高端 99 n')
jieba.add_word('塔綠班 99 n')                            ####要自己多增加常用字，這個是for 政黑板

with open('stops.txt', 'r', encoding='utf8') as f:  ####中文的停用字，我也忘記從哪裡拿到的，效果還可以，繁體字的資源真的比較少，大家將就一下吧
    stops = f.read().split('\n') 
stops.extend(['Re','討論','的','民黨','會','都','人'])
term1s = [t for t in pseg.cut(papers) if t not in stops]
#terms = [t for t in jieba.cut(papers) if t not in stops]
#print(type(terms))
terms=[]
for term1 in term1s:
    if term1.flag in ["n","nr"]:
        terms.append(term1.word)
#print(terms)
sorted(Counter(terms).items(), key=lambda x:x[1], reverse=True)
list_terms=Counter(terms)

keyword = "政治"
f=open("temp.json","w",encoding="utf-8")
nodes=list()
links=list()
i=0
for key,value in list_terms.items():
    #print(key)
    #print(value)
    if value > 1000: 
        group = 25
    elif value > 750:
        group = 20
    elif value > 500:
        group = 15
    elif value > 250:
        group = 10
    elif value > 100:
        group = 5
    else:
        group = 1

    if value > 1000: 
        color = 'rgba(255, 153, 51,1.0)'
    elif value > 750:
        color = 'rgba(252, 197, 68,0.85)'
    elif value > 500:
        color = 'rgba(252, 218, 68,0.75)'
    elif value > 250:
        color = 'rgba(247, 229, 106,0.7)'
    elif value > 100:
        color = 'rgba(250, 238, 127,0.65)'
    else:
        color = 'rgba(255, 247, 156,0.6)'
    if i < 20:
        nodes.append({"id": key, "group": group, "times": value, "color": color })
        links.append({"source": keyword, "target": key, "value": group})
    else:
        break
    i=i+1
sortna = sorted(nodes, key=lambda k: k['times'], reverse=True)
sortga = sorted(links, key=lambda k: k['value'], reverse=True)
json_data = {"nodes": sortna, "links": sortga}
json.dump(json_data,f,ensure_ascii=False,indent=4)
#print(type(terms))

font = 'SourceHanSansTW-Regular.otf'
my_wordcloud = WordCloud(background_color='black',font_path=font,relative_scaling=0.5).generate_from_frequencies(Counter(terms))#generate(words)

plt.imshow(my_wordcloud)
plt.axis("off")
plt.show()
#存檔
my_wordcloud.to_file('word_cloud.png')

######articut好像更好，但弄不出來，討厭