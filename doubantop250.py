# coding=utf-8
# @Time    : 2024/7/22 16:00
# #Author  : Ness Dawnastist
# @File    : spider.py
# @Software: VS Code

from bs4 import BeautifulSoup # 网页解析，获取数据
import re # 正则表达式，进行文字匹配
import urllib.request, urllib.error # 制定URL，获取网页数据
import xlwt # 进行excel操作
import sqlite3 # 进行SQLite数据库操作

"""
bs4(BeautifulSoup4)是一个用于解析HTML或XML文档的库
re 是一个Python的正则表达式库，正则表达式是一种文本匹配工具，可以用来搜索、替换以及解析字符串中的模式
urllib 用于处理URL，urllib.request是一个用于处理网络请求的模块
xlwt 用于操作excel
sqlite3 用于操作SQLite数据库
"""
def main():

    # 爬取网页
    baseurl = "https://movie.douban.com/top250?start="
    dataList = getData(baseurl)
    print(dataList)

def getData(baseurl):

    # 各种信息的正则表达式对象
    findLink = re.compile(r'<a href="(.*?)">')
    findImgSrc = re.compile(r'<img.*src="(.*?)"', re.S) #re.S 让换行符包含在字符串中
    findTitle = re.compile(r'<span class="title">(.*?)</span>')
    findRating = re.compile(r'<span class="rating_num" property="v:average">(.*?)</span>')
    findJudge = re.compile(r'<span>(\d*)人评价</span>')
    findInq = re.compile(r'<span class="inq">(.*?)</span>')
    findBd = re.compile(r'<p class="">(.*?)</p>', re.S)

    dataList = []
    for i in range(0, 10): # 网站总共有10页，逐一调取
        url = baseurl + str(i * 25)
        html = askURL(url)

        # 逐一解析数据
        soup = BeautifulSoup(html, "html.parser")
        # 查找符合要求的字符串，形成列表
        for item in soup.find_all("div", class_="item"):
            data = [] # 一部电影的所有信息
            item = str(item)
        
            # 获取影片详情
            link = re.findall(findLink, item)[0]
            data.append(link)
            imgSrc = re.findall(findImgSrc, item)[0]
            data.append(imgSrc)
            titles = re.findall(findTitle, item) 
            # 片名可能只有一个中文名，没有外文名
            if len(titles) == 2:
                ctitle = titles[0]
                data.append(ctitle)
                otitle = titles[1].replace("/", "") # 去掉无关的符号
                data.append(otitle)
            else :
                data.append(titles[0])
                data.append(" ") # 外国名留空，为了制表

            rating = re.findall(findRating, item)[0]
            data.append(rating)
            judgeNum = re.findall(findJudge, item)[0]
            data.append(judgeNum)
            inq = re.findall(findInq, item)
 
            if len(inq) != 0:
                inq = inq[0].replace("。", "") # 去掉句号
                data.append(inq)
            else:
                data.append(" ")
            bd = re.findall(findBd, item)[0]
            bd = re.sub("<br(\s+)?/>(\s+)?", " ", bd)
            bd = re.sub("/", " ", bd)
            data.append(bd.strip())
            dataList.append(data) # 处理好的一部电影信息放入datalist

    return dataList


def askURL(url): # 得到指定URL的网页内容
    # 模拟浏览器头部信息，向服务器发送请求
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0"
    }
    request = urllib.request.Request(url, headers=head)
    html = ""

    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")

    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)

    return html
    
if __name__ == '__main__':
    main()