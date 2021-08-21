#coding=utf-8
import requests as r
from lxml import etree
import time
from time import sleep
import random
a = random.uniform(36.3,36.7)
a = str(a)[:4:]
b = random.uniform(36.3,36.7)
b = str(b)[:4:]
c, d, e, f, g, h = '', '', '', '', '', ''
timetamp = time.mktime(time.localtime())
timetamp = int(timetamp)
url  = "http://xscfw.hebust.edu.cn/survey/ajaxLogin"
url2 = "http://xscfw.hebust.edu.cn/survey/index"  
url3 = f"http://xscfw.hebust.edu.cn/survey/surveySave?timestamp={timetamp}"
###
param = {"stuNum": "19L0252069","pwd": "0002223013","vcode": "",}
header = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36 Edg/90.0.818.62"}
###
try:
    response = r.post(url=url,params=param,headers=header)
    sleep(20)
    cookiesJAR = response.cookies
    cookies = cookiesJAR.get_dict()
    res = r.get(url=url2,headers=header,cookies=cookies,params=param)
    c = "登录正常，"
except:
    c = "登录失败，"
###
try:
    res.encoding = 'uft-8'
    html = etree.HTML(res.text)
    content = html.xpath('/html/body/ul/li[1]/div/span/text()')
    d = content[0]
except:
    d = "情况未知，"
###
try:
    url4 = 'http://xscfw.hebust.edu.cn/survey/index.action'
    rek = r.get(url=url4,cookies=cookies,headers=header)
    rek.encoding = 'utf-8'
    html3 =etree.HTML(rek.text)
    sid = html3.xpath('/html/body/ul/li[1]/@sid')[0]
    e = f"，获取sid：{sid}，"
except:
    e = "获取sid失败，"
###
try:
    url5 = f'http://xscfw.hebust.edu.cn/survey/surveyEdit?id={sid}'
    rej = r.get(url=url5,cookies=cookies,headers=header)
    sleep(5)
    rej.encoding = 'utf-8'
    html2 = etree.HTML(rej.text)
    stuId = html2.xpath('//*[@id="surveyForm"]/input[2]/@value')[0]
    qid = html2.xpath('//*[@id="surveyForm"]/input[3]/@value')[0]
    f = f"获取stuId:{stuId}，获取qid:{qid}，"
except:
    f = "获取stuId qid 失败，"   
####
try:
    data={
        "id":sid,
        "stuId":stuId,
        "qid":qid,
        "location":'',
        "c0":"不超过37.3℃，正常",
        "c1":a,
        "c3":"不超过37.3℃，正常",
        "c4":b,
        "c6":"健康",
        }
    g = "填写信息正常。"
except:
    g = "填写信息有误。"
####
if d == "已完成":
    h = "填报成功！"

elif d == "未完成":
    try:
        rep = r.post(url=url3, params=data, headers=header, cookies=cookies)
        h = "填报成功！"
    except:
        h = "请手动填写！"
else:
    h = "请手动填写！"
###
file=open("email.html",'w+',encoding='UTF-8')
file.write('体温'+a+'℃、'+b+'℃，'+h+'详细情况：'+c+d+e+f+g)
file.close()
