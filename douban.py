from bs4 import BeautifulSoup
import re
from urllib.request import urlopen
import csv
import time

start=time.clock()

def getData(url):
    findRating=re.compile(r'<strong class="ll rating_num" property="v:average">(.*)</strong>')
    findJudge=re.compile(r'<span property="v:votes">(\d*)</span>')
    findTime=re.compile(r'发行时间:</span>\s(\d{4}-*\d{0,2}-*\d{0,2})<br/>')
    findSinger=re.compile(r'sid=\d*">(.*?)</a>')
    remove=re.compile(r'                            |\n|</br>|\.*')
    removeblank=re.compile('\s{2,}')
    html=urlopen(url)
    soup = BeautifulSoup(html,"lxml")
    data=[]
    info=soup.find_all('div',id="info")
    info=str(info)
    info=re.sub(remove,"",info)
    info=re.sub(removeblank,"",info)
    title=soup.find("h1").text
    title=re.sub(remove,"",title)
    data.append(title)
    singer=re.findall(findSinger,info)[0]
    data.append(singer)
    time=re.findall(findTime,info)[0]
    data.append(time)
    item=soup.find_all('div',id="interest_sectl")
    item=str(item)
    rating=re.findall(findRating,item)[0]
    data.append(rating)
    try:
        judgeNum=re.findall(findJudge,item)[0]
        data.append(judgeNum)
    except:
        judgeNum=''
        data.append(judgeNum)
    return data

datalist=[]
for i in range(0,45,15):
    html=urlopen("https://music.douban.com/people/deadkingq/collect?start=%d"%i)
    soup = BeautifulSoup(html,"lxml")
    links=soup.findAll('div', attrs={'class' : 'pic'})
    for item in links:
        link=item.a['href']
        data=getData("%s"%link)
        datalist.append(data)

headers = ['专辑名','歌手','发行日期','豆瓣评分','评分人数']
with open('douban.csv','w') as f:
    f_csv = csv.writer(f)
    f_csv.writerow(headers)
    f_csv.writerows(datalist)
end=time.clock()
print(end-start)