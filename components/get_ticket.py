import requests
from bs4 import BeautifulSoup
from urllib.parse import unquote
import random

def process_url(rndNum):
    #抽淺草寺
    #將抽取變數拉到函數之外
    resUrl={}
    if rndNum<10 :
        rndNum='00'+str(rndNum)
    elif rndNum >99:
        rndNum='100'
    else:
        rndNum = '0'+str(rndNum)
    url = 'http://www.chance.org.tw/%E7%B1%A4%E8%A9%A9%E9%9B%86/%E6%B7%BA%E8%8D%89%E9%87%91%E9%BE%8D%E5%B1%B1%E8%A7%80%E9%9F%B3%E5%AF%BA%E4%B8%80%E7%99%BE%E7%B1%A4/%E7%B1%A4%E8%A9%A9%E7%B6%B2%E2%80%A7%E6%B7%BA%E8%8D%89%E9%87%91%E9%BE%8D%E5%B1%B1%E8%A7%80%E9%9F%B3%E5%AF%BA%E4%B8%80%E7%99%BE%E7%B1%A4__%E7%AC%AC021%E7%B1%A4.htm'
    decode = unquote(url)
    start_index = decode.index('__')
    data = decode[:start_index]
    code = f'__第{rndNum}籤.htm'
    new_url = (data + code).replace('http%3A//', 'http://')
    img_url = f'https://storage.googleapis.com/linebot01/img/{rndNum}.jpg'
    resUrl['Text_url'] = new_url
    resUrl['Img_url']=img_url
    return resUrl

def get_content(soup):
    data = soup.find_all('p')
    index = {}
    for i in range(len(data)):
        if '第' in data[i].getText() and i > 10:
            index['start_index'] = i
            break
    for i in range(len(data)):
        if '願望：'in data[i].getText():
            index['end_index']= i
            break
    res_data = data[index['start_index']:index['end_index']+1]
    res_content = [i.getText().strip().strip('\n') for i in res_data]

    return res_content


def get_ticket():
    rndNum = random.randint(1, 100)
    url = process_url(rndNum)
    try:
        res2 =requests.get(url['Text_url'])
        if res2.status_code == 200:
            html_content = res2.content.decode('big5', 'ignore')
            soup = BeautifulSoup(html_content, 'html.parser')
            if rndNum == 57:
                content = get_content(soup)[1:] #第57首格式有錯
            else:
                content = get_content(soup)

            res =[content,url['Img_url']]
            return res
    except Exception as e:
        return e

def process_good_url(rndNum):
    #抽快樂淺草寺
    resUrl={}
    if rndNum<10 :
        rndNum='00'+str(rndNum)
    elif rndNum >99:
        rndNum='100'
    else:
        rndNum = '0'+str(rndNum)
    url = 'http://www.chance.org.tw/%E7%B1%A4%E8%A9%A9%E9%9B%86/%E6%B7%BA%E8%8D%89%E9%87%91%E9%BE%8D%E5%B1%B1%E8%A7%80%E9%9F%B3%E5%AF%BA%E4%B8%80%E7%99%BE%E7%B1%A4/%E7%B1%A4%E8%A9%A9%E7%B6%B2%E2%80%A7%E6%B7%BA%E8%8D%89%E9%87%91%E9%BE%8D%E5%B1%B1%E8%A7%80%E9%9F%B3%E5%AF%BA%E4%B8%80%E7%99%BE%E7%B1%A4__%E7%AC%AC021%E7%B1%A4.htm'
    decode = unquote(url)
    start_index = decode.index('__')
    data = decode[:start_index]
    code = f'__第{rndNum}籤.htm'
    new_url = (data + code).replace('http%3A//', 'http://')
    img_url = f'https://storage.googleapis.com/linebot01/img/{rndNum}.jpg'
    resUrl['Text_url'] = new_url
    resUrl['Img_url']=img_url
    return resUrl

def get_good_ticket():
    num = [1, 2, 4, 6, 8, 9, 10, 11, 12, 13, 14, 16, 18, 19, 20, 21, 22, 23, 25, 26, 27, 29, 30, 31, 32, 33, 34, 35, 36,
           37, 38, 40, 41, 42, 43, 44, 45, 47, 48, 49, 50, 51, 53, 55, 56, 57, 60, 61, 62, 65, 68, 72, 73, 76, 78, 79,
           80, 81, 85, 86, 87, 89, 90, 91, 92, 93, 94, 95, 96, 99]
    rndNum = random.choice(num)
    url = process_good_url(rndNum)
    res2 =requests.get(url['Text_url'])
    if res2.status_code == 200:
        html_content = res2.content.decode('big5', 'ignore')
        soup = BeautifulSoup(html_content, 'html.parser')
        if rndNum == 57:
            content = get_content(soup)[1:]
        else:
            content = get_content(soup)
        res =[content,url['Img_url']]
        return res

def radar():
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