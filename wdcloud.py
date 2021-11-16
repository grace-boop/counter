########用dic過濾API找到出現最多次數的詞語,並輸出文字雲(以政黑板為例)#####
#######可以優化的:辭典可以加權限#####



import json
import matplotlib.pyplot as plt
from wordcloud import WordCloud
#from udicOpenData.dictionary import *##助教給的dictionary,後來沒用因為很醜
from PIL import Image
import jieba
import numpy as np
from collections import Counter
file = open("hateee.json",'r',encoding='utf-8')
papers = " "
###U have to follow the step to open the distinct file
###def wdcloud(file):
#print("lalala")
for line in file.readlines():
    dic=json.loads(line)
    article_title=dic['_source']['article_title']
    content=dic['_source']['content']
    papers=papers+article_title+content
#dump2es.py jieba
jieba.set_dictionary('2021-10-12 dict.txt.big.txt')
#print("lalala")
jieba.add_word('柯文哲')
jieba.add_word('陳時中')
jieba.add_word('張亞中')
jieba.add_word('朱立倫')
jieba.add_word('國民黨')
jieba.add_word('民眾黨')
jieba.add_word('民進黨')
jieba.add_word('台灣')
jieba.add_word('高端')
jieba.add_word('塔綠班')                            ####要自己多增加常用字，這個是for 政黑板

with open('stops.txt', 'r', encoding='utf8') as f:  ####中文的停用字，我也忘記從哪裡拿到的，效果還可以，繁體字的資源真的比較少，大家將就一下吧
    stops = f.read().split('\n') 
stops.extend(['Re','討論','「','的','民黨','會','都',' ','\n'])
terms = [t for t in jieba.cut(papers, cut_all=True) if t not in stops]
sorted(Counter(terms).items(), key=lambda x:x[1], reverse=True)
list_terms=Counter(terms)

keyword = "政治"
f=open("ccount.json","w",encoding="utf-8")
nodes=list()
links=list()
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
    nodes.append({"id": key, "group": group, "times": value, "color": color })
    links.append({"source": keyword, "target": key, "value": group})
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