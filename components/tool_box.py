import requests
from bs4 import BeautifulSoup
import random
import re


def radar():
    data =[]
    res_url=[]
    url = 'https://www.cwa.gov.tw/V8/C/W/OBS_Radar.html'
    res = requests.get(url)
    soup = BeautifulSoup(res.content,'html.parser')

    img_tags = soup.find_all('img')
    data = [i.get('src') for i in img_tags]
    res_url = ['https://www.cwa.gov.tw/'+data[1],'https://www.cwa.gov.tw/'+data[0]]
    return res_url

def randomspin():
    hit = random.randint(1, 61)
    url = f"https://iwnet.civil.taipei/SignedPoetry/Home/Detail/{hit}"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')

    poetry_div = soup.find('div', class_='main-poetry')
    poetry_text = poetry_div.get_text('\n', strip=True)
    process_text = [i.split('\n') for i in poetry_text.split('-')]
    process_data = []
    for i in process_text:
        for j in range(len(i)):
            process_data.append(i[j])

    res = '\n'.join(process_data)
    CHT = soup.find('div', class_='exp-body').get_text()
    data = [f'第{hit}籤\n',res, '\n',CHT]

    return data


def random_box(event):
    data = event.message.text
    pattern = r'^-隨機 \[.*\]$'
    random_box_match = re.match(pattern, data)
    if random_box_match:
        newdata = re.findall(r'\w+', data.split("[")[1].split("]")[0])
        res = f"隨機: {str(newdata)} \n 結果： {random.choice(newdata)}"
        return res
    else:
        return "格式錯誤 請依照 #-隨機 [ 項目 項目 ]# 使用/空白/或/,/分隔"