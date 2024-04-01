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
    todayFeature = soup.find_all('div', class_='TODAY_CONTENT')
    data = []
    for i in todayFeature:
        data.append(i.text)
    for i in today_word_elements:
        p_tags = i.find_all('p')
        for j in p_tags:
            data.append(j.text)

    return data


def astr_today(i):
    today = datetime.today().strftime('%Y-%m-%d')
    astro = ['牡羊座', '金牛座', '雙子座', '巨蟹座', '獅子座', '處女座', '天秤座', '天蠍座', '射手座', '魔羯座',
             '水瓶座', '雙魚座', ]
    index = astro.index(i)
    url = f'https://astro.click108.com.tw/daily_0.php?iAstro={index}&iAcDay={today}'

    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    today_word_elements = soup.find_all('div', class_='TODAY_WORD', )
    todayFeature = soup.find_all('div', class_='TODAY_CONTENT')
    data = []
    for i in todayFeature:
        data.append(i.text)
    for i in today_word_elements:
        p_tags = i.find_all('p')
        for j in p_tags:
            data.append(j.text)

    return data

