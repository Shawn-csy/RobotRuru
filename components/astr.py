import requests
from bs4 import BeautifulSoup
from datetime import datetime
import random

def astr(i):
    today = datetime.today().strftime('%Y-%m-%d')
    astro = ['牡羊座', '金牛座', '雙子座', '巨蟹座', '獅子座', '處女座', '天秤座', '天蠍座', '射手座', '魔羯座',
             '水瓶座', '雙魚座', ]
    index = astro.index(i)
    url = f'https://astro.click108.com.tw/weekly_1.php?iAcDay={today}&iType=1&iAstro={index}'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    today_word_elements = soup.find_all('div', class_='TODAY_WORD', )
    today_lucky_elements = soup.find_all('div', class_='TODAY_LUCKY')
    todayFeature = soup.find_all('div', class_='TODAY_CONTENT')
    data = []
    for i in todayFeature:
        data.append(i.text)
    for i in today_word_elements:
        p_tags = i.find_all('p')
        for j in p_tags:
            data.append(j.text)

    return data



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

randomspin()