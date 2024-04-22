import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json

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


def weeklyfate():
    #國師podcast內容
    url = "https://podcasts.apple.com/tw/podcast/%E5%94%90%E9%99%BD%E9%9B%9E%E9%85%92%E5%B1%8B/id1536374746"
    res = requests.get(url)
    def timedefine(podcasttime):
        date_time1 = datetime.today()
        date_string2 = podcasttime
        date_time2 = datetime.strptime(date_string2, "%Y年%m月%d日")
        difference = date_time1 - date_time2
        difference_days = difference.days
        return difference_days

    if res.status_code == 200:
        html_content = res.content.decode()
        soup = BeautifulSoup(html_content, 'html.parser')
        script_tag = soup.find("script", {"name": "schema:podcast-show"})

        if script_tag:
            try:
                json_data = script_tag.string
                podcast_info = json.loads(json_data)
                workdata = podcast_info['workExample']
                for i in workdata:
                    if "【本週提醒】" in i["name"]:
                        if timedefine(i["datePublished"]) < 8:
                            return i['description']
            except Exception as e :
                return e


